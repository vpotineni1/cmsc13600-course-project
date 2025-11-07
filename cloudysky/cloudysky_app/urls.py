
from django.urls import path
from . import views

urlpatterns = [
    path("time", views.time_central, name="time"),
    path("sum", views.sum, name="sum"),
    path("", views.index, name = "index"),
    path('login', views.login_new, name="login_new"),
    path("new", views.new, name="new_user"),
    path("createUser", views.createUser, name="createUser"),
]