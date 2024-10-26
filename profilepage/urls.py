from django.urls import path
from profilepage.views import profile_view

app_name = 'profilepage'

urlpatterns = [
    path('', profile_view, name='profile'),
]