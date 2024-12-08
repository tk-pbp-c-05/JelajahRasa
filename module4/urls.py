from django.urls import path
from module4.views import add_dish, check_dish, approve_dish, show_home, edit_rejected_dish, request_status, delete_dish, get_dish_data, edit_dish

app_name = 'module4'

urlpatterns = [
    path('add-dish', add_dish, name='add_dish'),
    path('check-dish', check_dish, name='check_dish'),
    path('show-home', show_home, name='show_home'),
    path('approve-dish/<uuid:dish_uuid>/', approve_dish, name='approve_dish'),
    path('edit-dish/<uuid:dish_uuid>/', edit_dish, name='edit_dish'),
    path('request-status/', request_status, name='request_status'),
    path('delete-dish/<uuid:dish_uuid>/', delete_dish, name='delete_dish'),
    path('get-dish-data/<uuid:dish_uuid>/', get_dish_data, name='get_dish_data'),
]