from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_results/', views.search_results, name='search_results'),
    path('artist_recommendation/', views.artist_recommendation, name='artist_recommendation'),
    path('tag_recommendation/', views.tag_recommendation, name='tags_recommendation'),
    path('album_recommendation/', views.album_recommendation, name='album_recommendation')
]
