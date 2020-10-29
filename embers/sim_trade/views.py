from django.shortcuts import render, HttpResponse
from django.http import Http404
from sim_trade import models
from datetime import datetime
import json
from django.http import JsonResponse
from django.core.serializers import serialize
# Create your views here.

def sim_trade(request):
    return render(request, 'sim_trade/sim_trade.html')

def table(request):
    return render(request, 'sim_trade/table.html')

def getOwned(request):
    queryset = models.Owned.objects.filter(userID=1)
    fields = ('ownedID', 'stockID', 'quantity', 'avg_price', 'min_price', 'max_price')
    res = json.loads(serialize('json', queryset, fields=fields))

    return JsonResponse(res,safe=False)
