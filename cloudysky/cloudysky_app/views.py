from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import JsonResponse
from zoneinfo import ZoneInfo
import datetime
from django.contrib.auth.models import User as AuthUser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import Role, Post, Comments, Media, User as AppUser

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

def get_app_user(django_user):
    app_user, _ = AppUser.objects.get_or_create(user=django_user)
    return app_user

@csrf_exempt
def createUser(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    email = request.POST.get("email", "")
    username = request.POST.get("username", "") or request.POST.get("user_name") or ""
    password = request.POST.get("password", "")
    is_admin = request.POST.get("is_admin", "0")

    if AuthUser.objects.filter(email = email).exists():
        return HttpResponse("Error: Email in Use", status = 400)
    
    user = AuthUser.objects.create_user(username=username, email=email, password=password)
    if is_admin == '1':
        user.is_staff = True
        user.is_superuser = True
    user.save()
    return redirect('login_new')

@csrf_exempt
def login_new(request):
    if request.method == "POST":
        username = request.POST.get("username", "") or request.POST.get("user_name") or ""
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            return render(request, 'registration/login.html',{'error': "Invalid username or password"})
    else:
        return render(request, 'registration/login.html')
    

@csrf_exempt
def new_post(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    return render(request, 'app/new_post.html'  )

@csrf_exempt
def new_comment(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    return render(request, 'app/new_comment.html'  )

@csrf_exempt
def createPost(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    content = request.POST.get("content", "")
    title = request.POST.get("title", "")
    media = Media.objects.create(title = title, content_text = content)
    author = get_app_user(request.user)
    
    Post.objects.create(content_id = media, creator = author)
    return HttpResponse("Posted", status = 201)

@csrf_exempt
def createComment(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    post_id = request.POST.get("post_id", "")
    content = request.POST.get("content", "")
    post = Post.objects.get(pk=post_id)
    author = get_app_user(request.user)

    Comments.objects.create(post_id = post, creator = author, comment_content=content)
    return HttpResponse("Posted", status = 201)

@csrf_exempt
def hideComment(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse("Unauthorized", status = 401)
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    comment_id = request.POST.get("comment_id", "")
    reason = request.POST.get("reason", "")
    comment = Comments.objects.get(pk = comment_id)
    comment.censored = True
    comment.censored_reason = reason
    comment.save()
    return HttpResponse("Hidden", status = 200)

@csrf_exempt
def hidePost(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)
    post_id = request.POST.get("post_id", "")
    reason = request.POST.get("reason", "") 
    post = Post.objects.get(pk=post_id)
    post.censored = True
    post.censored_reason = reason
    post.save()
    return HttpResponse("Hidden", status=200)

@csrf_exempt
def dumpFeed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    
    viewer = get_app_user(request.user)
    posts = Post.objects.all().order_by("post_id")
    obj = []

    for post in posts:
        username = post.creator.user.username
        media_obj = post.content_id  
        title = media_obj.title
        text  = media_obj.content_text


        post_reason = None

        if post.censored:
            if not(request.user.is_staff or post.creator == viewer):
                continue
            if post.censored_reason:
                post_reason = post.censored_reason

        post_comments = Comments.objects.filter(post_id=post).order_by("-add_time")

        comments_data = []
        for comment in post_comments:
            content = comment.comment_content
            comment_reason = None
            if comment.censored:
                if not(request.user.is_staff or comment.creator == viewer):
                    content = "This comment has been removed"
                else:
                    if comment.censored_reason:
                        comment_reason = comment.censored_reason
    
            comments_data.append({
                "id": comment.comment_id,
                "content": content,
                "creator": comment.creator.user.username,
                "time": comment.add_time.strftime("%Y-%m-%d %H:%M"),
                "reason": comment_reason,
            })

        obj.append({
            "id": post.post_id,
            "username": username,
            "date": post.add_time.strftime("%Y-%m-%d %H:%M"),
            "title": title,
            "content": text,
            "comments": comments_data,
            "reason": post_reason,
            })
    return JsonResponse(obj, safe=False)

@csrf_exempt
def feed(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    
    viewer = get_app_user(request.user)
    posts = Post.objects.all().order_by("post_id")
    obj = []

    for post in posts:
        username = post.creator.user.username
        if post.censored:
            if not(request.user.is_staff or post.creator == viewer):
                continue

        media_obj = post.content_id 
        text  = media_obj.content_text
        truncated = text[:100] + ("..." if len(text) > 100 else "")

        obj.append({
            "id": post.post_id,
            "username": username,
            "date": post.add_time.strftime("%Y-%m-%d %H:%M"),
            "title": media_obj.title,
            "Preview": truncated,
            })
    return JsonResponse(obj, safe=False)

@csrf_exempt
def feed_page(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    
    viewer = get_app_user(request.user)
    posts = Post.objects.all().order_by("post_id")
    obj = []

    for post in posts:
        username = post.creator.user.username
        if post.censored:
            if not(request.user.is_staff or post.creator == viewer):
                continue

        media_obj = post.content_id 
        text  = media_obj.content_text
        truncated = text[:100] + ("..." if len(text) > 100 else "")

        obj.append({
            "id": post.post_id,
            "username": username,
            "date": post.add_time.strftime("%Y-%m-%d %H:%M"),
            "title": media_obj.title,
            "Preview": truncated,
            })
    return render(request, "app/feed.html", {"posts": obj})

        
@csrf_exempt
def post_id(request, post_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    
    app_user = request.user

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)


    if post.censored:
        if request.user.is_staff:
            pass
        elif post.creator == app_user:
            pass 
        else:
            return HttpResponse("Post not found", status=404)
        
    media_obj = post.content_id 
    text  = media_obj.content_text
    
    posts = ({
        "id": post.post_id,
        "username": post.creator.user.username,
        "date": post.add_time.strftime("%Y-%m-%d %H:%M"),
        "title": media_obj.title,
        "Text": text,
    })

    comments = (Comments.objects.filter(post_id=post.post_id).order_by("comment_id"))
    obj = []

    for comment in comments:
        if comment.censored:
            if request.user.is_staff:
                content = comment.comment_content
            elif comment.creator == app_user:
                content = comment.comment_content
            else:
                content = "This comment has been removed"
        else:
            content = comment.comment_content
            
        obj.append({
            "id": comment.comment_id,
            "Comment_Creator": comment.creator.user.username,
            "date": comment.add_time.strftime("%Y-%m-%d %H:%M"),
            "Comment_Content": content,
        })
    return JsonResponse({"post": posts, "comments": obj,})


@csrf_exempt
def search_engine(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status = 401)
    query = request.GET.get("q","").strip()
    words = [word for word in query.split() if word]

    post_search_results = []
    comment_search_results = []

    if words:
        posts = Post.objects.all().order_by("post_id")
        for post in posts:
            media_obj = post.content_id 
            text  = media_obj.content_text
            title = media_obj.title

            for word in words:
                if (word in text) or (word in title):
                    post_search_results.append({
                        "id": post.post_id,
                        "username": post.creator.user.username,
                        "date": post.add_time.strftime("%Y-%m-%d %H:%M"),
                        "title": title,
                        "text": text,
                    })
                    break

        comments = (Comments.objects.all().order_by("comment_id"))
        for comment in comments:
            content = comment.comment_content
            content_lower = content.lower()
            for word in words:
                if (word in content_lower):
                    comment_search_results.append({
                        "id": comment.comment_id,
                        "Comment_Creator": comment.creator.user.username,
                        "date": comment.add_time.strftime("%Y-%m-%d %H:%M"),
                        "content":content,
                        })
                    break
    return render(request, 'app/search_engine.html',
        {
            "query" : query,
            "posts" : post_search_results,
            "comments": comment_search_results,
        }
    )