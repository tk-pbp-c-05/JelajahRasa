from django.urls import path
from profilepage.views import profile_view, edit_profile, all_favorite_dishes, get_user_data_api

app_name = 'profilepage'

urlpatterns = [
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/all-favorite-dishes/', all_favorite_dishes, name='all_favorite_dishes'),
    path('edit/<str:username>/', edit_profile, name='edit_profile'),
    path('api/user-data/<str:username>/', get_user_data_api, name='user_data_api'),
]
