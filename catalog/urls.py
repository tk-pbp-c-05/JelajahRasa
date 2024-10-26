from django.urls import path
from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('view-catalog', view_catalog, name='view_catalog'),

]