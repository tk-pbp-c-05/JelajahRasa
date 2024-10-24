from django.urls import path
from main.views import register

app_name = 'main'

urlpatterns = [
    path('register/', register, name='register'),
]