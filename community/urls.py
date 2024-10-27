from django.urls import path
from .views import community_home, add_comment, edit_comment, add_reply

app_name = 'community'

urlpatterns = [
    path('', community_home, name='home'),
    path('add_comment/', add_comment, name='add_comment'),
    path('edit_comment/<uuid:uuid>/', edit_comment, name='edit_comment'),
    path('add_reply/<uuid:comment_uuid>/', add_reply, name='add_reply'),
]