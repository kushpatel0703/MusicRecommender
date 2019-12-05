from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .util import *

def index(request):
    username = request.GET.get('Username', None)
    full_name = request.GET.get('Full Name', None)

    if username and full_name:
        if User.nodes.get_or_none(username = username) == None:
            User(username = username, name = full_name).save()

    users_list = []
    users = User.nodes.all()
    for user in users:
        users_list.append(user.username)
    context = {'users': users_list}
    return render(request, 'playlists/index.html', context)

def edit_account(request):
    tag_list, likes_list, dislikes_list = [], [], []
    if request.method == 'GET':
        type = request.GET.get('type', None)
        u = User.nodes.get(username = type)

        likes = request.GET.get('likes', None)
        if likes:
            t = Task.nodes.get(task = likes)
            u.likes.connect(t)

        dislikes = request.GET.get('dislikes', None)
        if dislikes:
            t = Task.nodes.get(task = dislikes)
            u.dislikes.connect(t)

        dislikes_remove = request.GET.get('remove_dislikes', None)
        if dislikes_remove:
            t = Task.nodes.get(task = dislikes_remove)
            u.dislikes.disconnect(t)

        likes_remove = request.GET.get('remove_likes', None)
        if likes_remove:
            t = Task.nodes.get(task = likes_remove)
            u.likes.disconnect(t)

        tags = Task.nodes.all()
        for t in tags:
            tag_list.append(t.task)

        u.refresh()
        user_likes = u.likes
        for ul in user_likes:
            likes_list.append(ul.task)

        user_dislikes = u.dislikes
        for ul in user_dislikes:
            dislikes_list.append(ul.task)

    context = {'username': type, 'tags': tag_list, 'likes_list': likes_list, 'dislikes_list': dislikes_list}
    return render(request, 'playlists/edit_account.html', context)

def recommendations(request):
    if request.method == 'GET':
        user1 = request.GET.get('user1', None)
        user2 = request.GET.get('user2', None)
        user3 = request.GET.get('user3', None)
        user_list = [User.nodes.get(username = user1), User.nodes.get(username = user2), User.nodes.get(username = user3)]

        likes_list = generate_likes(user_list)
        artist_recommendation, album_recommendation = generate_reccomendations(likes_list)

        context = {'user1': user1, 'user2': user2, 'user3': user3, 'artist_recommendations': artist_recommendation, 'album_recommendation': album_recommendation}
        return render(request, 'playlists/recommendations.html', context)
