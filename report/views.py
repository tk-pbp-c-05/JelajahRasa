from django.shortcuts import render, redirect, get_object_or_404
from report.forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Food
from .models import Report
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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

@csrf_exempt
def api_create_report(request, food_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            food = get_object_or_404(Food, uuid=food_id)
            print("AAAAAAAA")
            print(food)
            form = ReportForm(data)
            if form.is_valid():
                report = form.save(commit=False)
                report.food = food
                report.reported_by = request.user
                report.save()
                return JsonResponse({
                    "status": True,
                    "message": "Report created successfully!"
                }, status=201)
            return JsonResponse({
                "status": False,
                "message": "Invalid form data",
                "errors": form.errors
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
def api_report_list(request):
    reports = Report.objects.select_related('food', 'reported_by').all()
    data = []
    for report in reports:
        data.append({
            "model": "report.report",
            "pk": report.id,
            "fields": {
                "food": report.food.name,
                "reported_by": report.reported_by.id,
                "issue_type": report.issue_type,
                "description": report.description,
                "created_at": report.created_at.isoformat(),
                "status": report.status
            }
        })
    return JsonResponse({"status": True, "data": data})


@csrf_exempt
def api_update_report_status(request, report_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report = get_object_or_404(Report, id=report_id)
            status = data.get('status')

            if status not in ['approved', 'rejected']:
                return JsonResponse({
                    "status": False,
                    "message": "Invalid status value"
                }, status=400)

            report.status = status
            report.save()

            return JsonResponse({
                "status": True,
                "message": f"Report {status} successfully"
            })
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
def api_delete_report(request, report_id):
    if request.method == 'POST':
        try:
            report = get_object_or_404(Report, id=report_id)

            if report.status not in ['approved', 'rejected']:
                return JsonResponse({
                    "status": False,
                    "message": "Report can't be deleted"
                }, status=400)

            report.delete()
            return JsonResponse({
                "status": True,
                "message": "Report deleted successfully"
            })
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)
    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=405)