import requests
from requests_html import HTMLSession

k = "2be158c9062bcc8c01bf34c4a014e010"
s = "c6b427a6d36a63e8f28b4850758efe71"
b = 'http://ws.audioscrobbler.com/2.0/'

def artist_search(artist):
    ret_list = []
    url = b +'?method=artist.search&format=json&artist='+ artist + '&api_key='+ k + '&limit=50'
    data = requests.get(url).json()['results']['artistmatches']['artist']
    for d in data:
        if d['mbid'] != '':
            ret_list.append((d['name'], d['mbid']))
    return ret_list

def artist_info(mbid):
    ret_list = []
    url = b +'?method=artist.getinfo&format=json&mbid='+ mbid + '&api_key='+ k
    data = requests.get(url).json()['artist']
    return data

def album_search(album):
    ret_list = []
    url = b +'?method=album.search&format=json&album='+ album + '&api_key='+ k + '&limit=50'
    data = requests.get(url).json()['results']['albummatches']['album']
    for d in data:
        if d['mbid'] != '':
            ret_list.append((d['name'], d['artist'], d['mbid']))
    return ret_list

def album_info(mbid):
    ret_list = []
    url = b +'?method=album.getinfo&format=json&mbid='+ mbid + '&api_key='+ k
    data = requests.get(url).json()['album']
    return data
