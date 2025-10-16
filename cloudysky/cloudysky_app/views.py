from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime
from zoneinfo import ZoneInfo

def time_central(request):
    if request.method == "GET": 
        time_CDT = datetime.now(ZoneInfo("America/Chicago"))
        return HttpResponse(time_CDT.strftime("%H:%M"), status = 200)

def sum(request):
    if request.method == "GET":
        n1 = request.GET.get('n1')
        n2 = request.GET.get('n2')
        sum = float(n1) + float(n2)
        return HttpResponse(str(sum), status = 200)