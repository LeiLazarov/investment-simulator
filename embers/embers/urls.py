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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about_us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('contact_us/', TemplateView.as_view(template_name='contact_us.html'), name='contact_us'),
    path('', include('login.urls')),
    path('', include('tutorial.urls')),
    path('', include('sim_trade.urls')),
    path('', include('watchlist.urls')),
    path('', include('stock.urls')),
    path('', include('statistic.urls')),

    # server是一个视图函数server(request, path), 通过path找到文件然后返回response
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
