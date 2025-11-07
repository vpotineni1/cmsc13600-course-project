"""
URL configuration for cloudysky project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cloudysky_app import views as app_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include('cloudysky_app.urls')),
    path('', app_views.root_redirect, name = 'root_redirect'),
    path('accounts/login/', app_views.login_new, name = 'login'),
    path('index.html',app_views.index, name ='index.html'),

]