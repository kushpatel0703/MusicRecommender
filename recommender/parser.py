from .last_fm_interface import *
from .models import *
from playlists.models import *
from django.db import connection

def artist_recommendation_parser(mbid):
    tag_list, ret_list = [], []
    check = Artist.objects.raw('SELECT * FROM recommender_artist WHERE mbid = %s', [mbid])
    if not check:
        tag_list = add_artist(mbid)
    else:
        seen_tags = Artist.objects.raw('SELECT * FROM recommender_artisttag t INNER JOIN recommender_artist a ON a.id = t.art_id WHERE mbid = %s', [mbid])
        for t in seen_tags:
            tag_list.append(t.tag)

    query = generate_reccomender_query(len(tag_list), 'artist')
    top_artists = Artist.objects.raw(query, tag_list)
    for t in top_artists:
        ret_list.append(t.name)

    return ret_list

def album_recommendation_parser(mbid):
    tag_list, ret_list = [], []
    check = Album.objects.raw('SELECT * FROM recommender_album WHERE mbid = %s', [mbid])
    if not check:
        info = album_info(mbid)
        name = info['name']
        mbid = info['mbid']
        image = info['image'][1]['#text']
        artist_mbid = info['tracks']['track'][0]['artist']['mbid']

        artist_check = Album.objects.raw('SELECT * FROM recommender_artist WHERE mbid = %s', [artist_mbid])
        if not artist_check:
            add_artist(artist_mbid)
            artist_check = Album.objects.raw('SELECT * FROM recommender_artist WHERE mbid = %s', [artist_mbid])

        connection.cursor().execute('INSERT INTO recommender_album (name, mbid, image, primary_artist_id) VALUES (%s, %s, %s, %s)', [name, mbid, image, artist_check[0].id])
        check = Album.objects.raw('SELECT * FROM recommender_album WHERE mbid = %s', [mbid])
        min_tags = min(len(info['tags']['tag']), 5)

        for i in range(min_tags):
            curr_tag = info['tags']['tag'][i]['name']
            if not Task.nodes.get_or_none(task = curr_tag):
                Task(task = curr_tag).save()
            tag_list.append(curr_tag)
            connection.cursor().execute('INSERT INTO recommender_albumtag (al_id, tag) VALUES (%s, %s)', [check[0].id, curr_tag])
    else:
        seen_tags = Album.objects.raw('SELECT * FROM recommender_albumtag t INNER JOIN recommender_album a ON a.id = t.al_id WHERE mbid = %s', [mbid])
        for t in seen_tags:
            tag_list.append(t.tag)

    query = generate_reccomender_query(len(tag_list), 'album')
    top_albums = Album.objects.raw(query, tag_list)
    for t in top_albums:
        ret_list.append(t.name)

    return ret_list

def tags_to_artist(tag_list):
    ret_list = []
    query = generate_reccomender_query(len(tag_list), 'artist')
    top_artist = Artist.objects.raw(query, tag_list)
    for t in top_artist:
        ret_list.append(t.name)

    return ret_list

def tags_to_albums(tag_list):
    ret_list = []
    query = generate_reccomender_query(len(tag_list), 'album')
    top_albums = Album.objects.raw(query, tag_list)
    for t in top_albums:
        ret_list.append(t.name)

    return ret_list

def add_artist(mbid):
    tag_list = []
    info = artist_info(mbid)
    name = info['name']
    mbid = info['mbid']
    image = info['image'][1]['#text']

    connection.cursor().execute('INSERT INTO recommender_artist (name, mbid, image) VALUES (%s, %s, %s)', [name, mbid, image])
    check = Artist.objects.raw('SELECT * FROM recommender_artist WHERE mbid = %s', [mbid])
    min_tags = min(len(info['tags']['tag']), 5)

    for i in range(min_tags):
        curr_tag = info['tags']['tag'][i]['name']
        if not Task.nodes.get_or_none(task = curr_tag):
            Task(task = curr_tag).save()
        tag_list.append(curr_tag)
        connection.cursor().execute('INSERT INTO recommender_artisttag (art_id, tag) VALUES (%s, %s)', [check[0].id, curr_tag])

    return tag_list

def generate_reccomender_query(n, type):
    s = ''
    b = ' GROUP BY a.name ORDER BY count(*) DESC'

    if type == 'artist':
        s += 'SELECT * FROM recommender_artisttag t INNER JOIN recommender_artist a ON a.id = t.art_id'
    else:
        s += 'SELECT * FROM recommender_albumtag t INNER JOIN recommender_album a ON a.id = t.al_id'

    for i in range(n):
        if i == 0:
            s += ' WHERE tag = %s'
        else:
            s += ' OR tag = %s'

    s += b
    return s

def get_albums():
    ret_list = []
    albums = Album.objects.raw('SELECT * FROM recommender_album')

    for a in albums:
        ret_list.append(a.name)

    return ret_list

def get_tags():
    ret_list = set()
    tags = Album.objects.raw('SELECT * FROM recommender_albumtag')

    for a in tags:
        if a.tag not in ret_list:
            ret_list.add(a.tag)

    tags = Album.objects.raw('SELECT * FROM recommender_artisttag')

    for a in tags:
        if a.tag not in ret_list:
            ret_list.add(a.tag)

    return sorted(list(ret_list))

def album_delete(name):
    check = Album.objects.raw('SELECT * FROM recommender_album WHERE name = %s', [name])
    connection.cursor().execute('DELETE FROM recommender_albumtag WHERE al_id = %s', [check[0].id])
    connection.cursor().execute('DELETE FROM recommender_album WHERE name = %s', [name])

def album_update(name, new_name):
    connection.cursor().execute('UPDATE recommender_album SET name = %s WHERE name = %s', [new_name, name])
