# MyFavoriteDishes/urls.py

from django.urls import path
from .views import show_favorite, add_favorite_dish, edit_favorite_dish, delete_favorite_dish, add_favorite, add_fav_dish_ajax, show_json, access_favorite, show_json_flutter, add_favdish_flutter, delete_favorite_dish_flutter, edit_favdish_flutter, get_foodlist_flutter, select_favdish_flutter

app_name = 'MyFavoriteDishes'

urlpatterns = [
    path('', show_favorite, name='show_favorite'),
    path('favorite/', access_favorite, name='access_favorite'),
    path('add-fav/', add_favorite_dish, name='add_favorite_dish'),
    path('edit-fav-dish/<uuid:uuid>/', edit_favorite_dish, name='edit_favorite_dish'),
    path('delete/<uuid:uuid>', delete_favorite_dish, name='delete_favorite_dish'),
    path('add-fav-from-catalogue/', add_favorite, name='add_favorite'),
    path('add-fav-dish-ajax/', add_fav_dish_ajax, name='add_fav_dish_ajax'),
    path('jsonfilter/', show_json, name='show_json'),
    path('json/', show_json_flutter, name='show_json_flutter'),
    path('addfavdish-flutter/', add_favdish_flutter, name='add_favdish_flutter'),
    path('delete-flutter/<uuid:uuid>/', delete_favorite_dish_flutter, name='delete_favorite_dish_flutter'),
    path('edit-flutter/<uuid:uuid>/', edit_favdish_flutter, name='edit_favdish_flutter'),
    path('getfood-json/', get_foodlist_flutter, name='get_foodlist_flutter'),
    path('select-favdish-flutter/', select_favdish_flutter, name='select_favdish_flutter'),
]

