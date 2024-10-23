from django.urls import path
from module4.views import show_home, add_dish

app_name = 'module4'

urlpatterns = [
    path('', show_home, name='show_home'),
    path('add-dish', add_dish, name='add_dish'),
]