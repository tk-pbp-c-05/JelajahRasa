from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('food/<str:food_id>/', report_issue, name='report_issue'),
    path('reports/', report_list, name='report_list'),
    path('<int:report_id>/approve/', approve_report, name='approve_report'),
    path('<int:report_id>/reject/', reject_report, name='reject_report'),

    path('api/food/<str:food_id>/report/', api_create_report, name='api_create_report'),
    path('api/reports/<str:report_id>/delete/', api_delete_report, name='api_delete_report'),
    path('api/reports/', api_report_list, name='api_report_list'),
    path('api/reports/<int:report_id>/status/', api_update_report_status, name='api_update_report_status'),
]