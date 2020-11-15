"""embers URL Configuration

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
from django.urls import path, re_path

from . import views

app_name = 'stock'

urlpatterns = [
    re_path(r'^stock/(.+)/$', views.stock, name='stock'),
    re_path(r'^search/(.+)/$', views.search, name='search'),
    re_path(r'^post_follow/(.+)/$', views.post_follow, name='post_follow'),
]
