import requests
from django.shortcuts import render
from statistic import models
import json
from django.http import HttpResponse
from django.core.serializers import serialize

def table(request):
    return render(request, 'sim_trade/table.html')

