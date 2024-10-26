from django.urls import path
from profilepage.views import profile_view, edit_profile

app_name = 'profilepage'

urlpatterns = [
    path('<str:username>/', profile_view, name='profile'),
    path('edit/<str:username>/', edit_profile, name='edit_profile'),
]
