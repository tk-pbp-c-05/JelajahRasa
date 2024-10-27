from django.urls import path
from .views import community_home, add_comment, edit_comment, add_reply, delete_comment, delete_reply, comment_detail

app_name = 'community'

urlpatterns = [
    path('', community_home, name='home'),
    path('add_comment/', add_comment, name='add_comment'),
    path('edit_comment/<uuid:uuid>/', edit_comment, name='edit_comment'),
    path('add_reply/<uuid:comment_uuid>/', add_reply, name='add_reply'),
    path('delete_comment/<uuid:uuid>/', delete_comment, name='delete_comment'),
    path('delete_reply/<uuid:uuid>/', delete_reply, name='delete_reply'),
    path('comment/<uuid:uuid>/', comment_detail, name='comment_detail'),
]
