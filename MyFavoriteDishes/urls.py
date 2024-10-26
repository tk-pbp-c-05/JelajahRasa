# MyFavoriteDishes/urls.py

from django.urls import path
from .views import show_favorite, add_favorite_dish, edit_favorite_dish, delete_favorite_dish, add_favorite, add_fav_dish_ajax, show_json, access_favorite

app_name = 'MyFavoriteDishes'

urlpatterns = [
    path('', show_favorite, name='show_favorite'),
    path('favorite/', access_favorite, name='access_favorite'),
    path('add-fav/', add_favorite_dish, name='add_favorite_dish'),
    path('edit-fav-dish/<uuid:uuid>/', edit_favorite_dish, name='edit_favorite_dish'),
    path('delete/<uuid:uuid>', delete_favorite_dish, name='delete_favorite_dish'),
    path('add-fav-from-catalogue/', add_favorite, name='add_favorite'),
    path('add-fav-dish-ajax/', add_fav_dish_ajax, name='add_fav_dish_ajax'),
    path('json/', show_json, name='show_json')
]
