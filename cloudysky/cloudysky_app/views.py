from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from zoneinfo import ZoneInfo
import datetime
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login




def time_central(request):
    if request.method == "GET": 
        time_CDT = datetime.datetime.now(ZoneInfo("America/Chicago"))
        return HttpResponse(time_CDT.strftime("%H:%M"), status = 200)

def sum(request):
    if request.method == "GET":
        n1 = request.GET.get('n1')
        n2 = request.GET.get('n2')
        sum = float(n1) + float(n2)
        return HttpResponse(str(sum), status = 200)
    
def index(request):
    current_time = datetime.datetime.now(ZoneInfo("America/Chicago"))
    time_str = current_time.strftime('%H:%M')
    return render(request, 'app/index.html', context={'current_time':time_str})

def new(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "app/new.html")

@csrf_exempt
def createUser(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    email = request.POST.get("email", "")
    username = request.POST.get("user_name", "")
    password = request.POST.get("password", "")
    is_admin = request.POST.get("is_admin", "0")

    if User.objects.filter(email = email).exists():
        return HttpResponse("Error: Email in Use", status = 400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    if is_admin == '1':
        user.is_staff = True
        user.is_superuser = True
    user.save()
    return redirect('login_new')

def login_new(request):
    if request.method == "POST":
        username = request.POST.get("user_name", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            return render(request, 'registration/login.html',{'error': "Invalid username or password"})
    else:
        return render(request, 'registration/login.html')

        



    