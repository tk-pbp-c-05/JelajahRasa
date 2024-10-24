# MyFavoriteDishes/urls.py

from django.urls import path
from .views import show_favorite, add_favorite_dish, edit_favorite_dish, delete_favorite_dish, add_favorite

app_name = 'MyFavoriteDishes'

urlpatterns = [
    path('', show_favorite, name='show_favorite'),
    path('add-fav/', add_favorite_dish, name='add_favorite_dish'),
    path('edit-fav-dish/<uuid:id>/', edit_favorite_dish, name='edit_favorite_dish'),
    path('delete/<uuid:id>', delete_favorite_dish, name='delete_favorite_dish'),
    path('add-fav-from-catalogue/', add_favorite, name='add_favorite'),
]
