
from django.urls import path
from . import views

urlpatterns = [
    path("time", views.time_central, name="time"),
    path("sum", views.sum, name="sum"),
    path("", views.index, name = "index"),
    path('login', views.login_new, name="login_new"),
    path("accounts/login/", views.login_new, name="login_new"),
    path("new", views.new, name="new_user"),
    path("createUser/", views.createUser, name="create_user"),
    path('new_post', views.new_post, name='new_post'),
    path('new_comment', views.new_comment, name='new_comment'),
    path("createPost/", views.createPost, name = 'create_post'),
    path("createPost", views.createPost, name = 'create_post'),
    path("createComment/", views.createComment, name = 'create_comment'),
    path("createComment", views.createComment, name = 'create_comment'),
    path("hideComment/", views.hideComment, name = 'hide_comment'),
    path("hideComment", views.hideComment, name = 'hide_comment'),
    path("hidePost/", views.hidePost, name = 'hide_post'),
    path("hidePost", views.hidePost, name = 'hide_post'),
    path("dumpFeed/", views.dumpFeed, name = 'dumpFeed'),
    path("dumpFeed", views.dumpFeed, name = 'dumpFeed'),
    path("feed", views.feed, name = 'feed'),
]


