from .models import *
from recommender.parser import *

def generate_likes(users_list):
    d = {}

    for u in users_list:
        for l in u.likes:
            if l.task in d:
                d[l.task] += 1
            else:
                d[l.task] = 1

    for u in users_list:
        for l in u.dislikes:
            if l.task in d:
                d[l.task] -= 1
            else:
                d[l.task] = -1

    return sorted(d.items(), reverse = True, key=lambda x: x[1])

def generate_reccomendations(likes_list):
    new_list = []
    num = min(5, len(likes_list))

    for i in range(num):
        new_list.append(likes_list[i][0])

    album_recommendation = tags_to_albums(new_list)
    artist_recommendation = tags_to_artist(new_list)

    return artist_recommendation, album_recommendation
