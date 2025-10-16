

from django.urls import path
from . import views

urlpatterns = [
    path("time", views.time_central, name="time"),
    path("sum", views.sum, name="sum"),
]