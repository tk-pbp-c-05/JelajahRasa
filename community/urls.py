from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('edit_comment/<uuid:uuid>/', views.edit_comment, name='edit_comment'),
    path('add_reply/<uuid:comment_uuid>/', views.add_reply, name='add_reply'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]