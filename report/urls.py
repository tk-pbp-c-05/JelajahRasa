from django.urls import path
from report.views import *

app_name = 'report'

urlpatterns = [
    path('food/<str:food_id>/', report_issue, name='report_issue'),
    path('reports/', report_list, name='report_list'),
    path('<int:report_id>/approve/', approve_report, name='approve_report'),
    path('<int:report_id>/reject/', reject_report, name='reject_report'),
]