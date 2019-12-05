from django.http import HttpResponse
from django.shortcuts import render
from .last_fm_interface import *
from .parser import *

def index(request):
    key = request.GET.get('type', None)
    if key and key[-1] == "u":
        new_name = request.GET.get('new_name', None)
        album_update(key[0:len(key) - 2], new_name)
    elif key and key[-1] == "d":
        album_delete(key[0:len(key) - 2])

    albums = get_albums()
    tags = get_tags()
    context = {'albums': albums, 'tags': tags}
    return render(request, 'recommender/index.html', context)

def search_results(request):
    if request.method == 'GET':
        key = request.GET.get('textfield', None)
        type = request.GET.get('type', None)
        if type == "artist":
            context = {'artist_list': artist_search(key)}
            return render(request, 'recommender/search_results_artist.html', context)
        elif type == "album":
            context = {'album_list': album_search(key)}
            return render(request, 'recommender/search_results_album.html', context)

def tag_recommendation(request):
    tag_list = []
    if request.method == 'GET':
        tag_list.append(request.GET.get('t1', None))
        tag_list.append(request.GET.get('t2', None))
        tag_list.append(request.GET.get('t3', None))
        recommended_artists = tags_to_artist(tag_list)
        recommended_albums = tags_to_albums(tag_list)

        context = {'artists': recommended_artists, 'albums': recommended_albums}
        return render(request, 'recommender/tag_recommendation.html', context)

def artist_recommendation(request):
    if request.method == 'GET':
        mbid = request.GET.get('mbid', None)
        recommended_artists = artist_recommendation_parser(mbid)
        context = {'recommended_artists': recommended_artists}
        return render(request, 'recommender/recommended_artists.html', context)

def album_recommendation(request):
    if request.method == 'GET':
        mbid = request.GET.get('mbid', None)
        recommended_albums = album_recommendation_parser(mbid)
        context = {'recommended_albums': recommended_albums}
        return render(request, 'recommender/recommended_albums.html', context)
