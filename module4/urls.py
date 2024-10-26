from django.urls import path
from module4.views import add_dish, check_dish, approve_dish, show_home

app_name = 'module4'

urlpatterns = [
    path('add-dish', add_dish, name='add_dish'),
    path('check-dish', check_dish, name='check_dish'),
    path('show-home', show_home, name='show_home'),
    path('approve-dish/<uuid:dish_uuid>/', approve_dish, name='approve_dish'),
    
]