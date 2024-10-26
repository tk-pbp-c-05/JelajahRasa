from django.shortcuts import render, redirect, get_object_or_404
from report.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Food
from .models import Report
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
        
@login_required
def report_issue(request, food_id):

    if request.method == 'POST':
        food = get_object_or_404(Food, uuid=food_id)
        data = json.loads(request.body)
        form = ReportForm(data)
        if form.is_valid():
            report = form.save(commit=False)
            report.food = food
            report.reported_by = request.user
            report.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False,"errors":form.errors},status=400)
    
    return JsonResponse({"error":"Invalid request"},status=400)

# approve/reject report only by admin
@require_POST
@login_required
def approve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'approved'
    report.save()
    return JsonResponse({'success': True, 'status': report.status})

@require_POST
@login_required
def reject_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'rejected'
    report.save()
    return JsonResponse({'success': True, 'status': report.status})

@login_required
def report_list(request):
    reports = Report.objects.select_related('food','reported_by').all()
    return render(request, 'report_list.html', { 'reports': reports})
