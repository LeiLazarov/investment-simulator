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
from django.conf.urls import url

from . import views

app_name = 'sim_trade'

urlpatterns = [
    # path('sim_trade/<str:symbol>', views.sim_trade, name='sim_trade'),
    path('sim_trade/', views.table, name='sim_trade'),
    re_path(r'sim_trade/getOwned/', views.getOwned, name='getOwned'),
    re_path(r'sim_trade/checkStock/(.+)/$', views.checkStock, name='checkStock'),
    re_path(r'sim_trade/sellCheckStock/(.+)/$', views.sellCheckStock, name='sellCheckStock'),
    url(r'^buy_stock$', views.buy_stock),
    url(r'^sell_stock$', views.sell_stock),
]
