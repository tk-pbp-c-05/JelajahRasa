from django.urls import path
from module4.views import add_dish, check_dish, approve_dish, show_home, edit_rejected_dish, request_status, delete_dish, get_dish_data, edit_dish, show_json, flutter_add_dish, flutter_delete_rejected_dish, flutter_edit_rejected_dish, flutter_get_dish_detail, flutter_get_pending_dishes, flutter_get_user_dishes, flutter_approve_dish

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
    path('show-json', show_json, name='show_json'),
    path('flutter-add-dish/', flutter_add_dish, name='flutter_add_dish'),
    path('flutter-delete-rejected-dish/<uuid:dish_uuid>/', flutter_delete_rejected_dish, name='flutter_delete_rejected_dish'),
    path('flutter-edit-rejected-dish/<uuid:dish_uuid>/', flutter_edit_rejected_dish, name='flutter_edit_rejected_dish'),
    path('flutter-get-dish-detail/<uuid:dish_uuid>/', flutter_get_dish_detail, name='flutter_get_dish_detail'),
    path('flutter-get-pending-dishes/', flutter_get_pending_dishes, name='flutter_get_pending_dishes'),
    path('flutter-get-user-dishes/', flutter_get_user_dishes, name='flutter_get_user_dishes'),
    path('flutter-approve-dish/<uuid:dish_uuid>/', flutter_approve_dish, name='flutter_approve_dish'),
]