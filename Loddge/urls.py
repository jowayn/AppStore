"""Loddge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.landing, name='landing'),
    path('home/', app.views.home, name='home'),
    path('marketplace/', app.views.marketplace, name='marketplace'),
    path('marketplace/add/', app.views.add, name='add'),
    path('marketplace/view/<str:id>', app.views.view, name='view'),
    path('marketplace/edit/<str:id>', app.views.edit, name='edit'),
    path('reservations/', app.views.reservations, name='reservations'),
    path('register/', app.views.register, name='register'),
    path('login/', app.views.login, name='login'),
    path('admin/', app.views.admin, name='admin')
] 
