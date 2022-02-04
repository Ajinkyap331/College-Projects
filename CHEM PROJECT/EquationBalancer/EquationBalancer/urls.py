"""EquationBalancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView
from home import views


urlpatterns = [
    path("admin", admin.site.urls),
    # path("", views.index, name='home'),
    path("", TemplateView.as_view(template_name='index.html')),
    path("contact", views.contact, name='contact'),
    path("equation", views.equation, name='equation'),
    path("periodic", views.periodic, name='periodic'),
    path("mass", views.mass, name='mass'),
    path("numericals", views.numericals, name='numericals'),
    path("gcv", views.gcv, name='gcv'),
    path("hardness", views.hardness, name='hardness'),
    path("coal", views.coal, name='coal'),
]
