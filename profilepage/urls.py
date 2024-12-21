from django.urls import path
from profilepage.views import profile_view, edit_profile, all_favorite_dishes
from profilepage.views import get_user_profile_api, get_user_favorites_api, get_user_reviews_api, get_user_comments_api

app_name = 'profilepage'

urlpatterns = [
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/all-favorite-dishes/', all_favorite_dishes, name='all_favorite_dishes'),
    path('edit/<str:username>/', edit_profile, name='edit_profile'),
    path('api/user-profile/<str:username>/', get_user_profile_api, name='user_profile_api'),
    path('api/user-favorites/<str:username>/', get_user_favorites_api, name='user_favorites_api'),
    path('api/user-reviews/<str:username>/', get_user_reviews_api, name='user_reviews_api'),
    path('api/user-comments/<str:username>/', get_user_comments_api, name='user_comments_api'),
]
