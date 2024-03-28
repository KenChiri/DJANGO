from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import EmergencyReportForm
from .models import EmergencyReport
from django.core import serializers
from django.contrib import messages


User = get_user_model()



def report_emergency(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your report has been sent. Thank you!')
            
    else:
        form = EmergencyReportForm()
    return render(request, 'emergency/home.html', {'form': form})



def accident_alerts(request):
    reports = EmergencyReport.objects.order_by('-created_at')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = serializers.serialize('json', reports)
        return JsonResponse(data, safe=False)
    else:
        return render(request, 'emergency/accident_alerts.html', {'reports': reports})


def abstract (request):
    return render(request, 'emergency/abstract.html')


def charges (request):
    return render(request, 'emergency/chargesheet.html')

def medical (request):
    return render(request, 'emergency/medicalreport.html')
