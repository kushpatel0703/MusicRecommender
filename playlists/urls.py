from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_account/', views.edit_account, name = 'edit_account'),
    path('recommendations/', views.recommendations, name = 'recommendations')
]
