from django.urls import path
from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('', view_catalog, name='view_catalog'),
]