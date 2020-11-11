import requests

from django.shortcuts import render, redirect
from sim_trade import models as sim_models

import json
from django.http import HttpResponse
from django.core.serializers import serialize

from stock import models as stock_models

def table(request):
    return render(request, 'sim_trade/table.html')



def account_record(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    #uid = 1
    record_account = sim_models.Record.objects.filter(user_id=uid).values()
    record_list = []
    
    for e in record_account:
        record = {}
        record['id'] = e['id']
        record['stockname'] = stock_models.Stock.objects.get(id= e['stock_id']).symbol
        record['quantity'] = e['quantity']
        record['price'] = e['price']
        record['type'] = 'sell' if e['type'] == True else 'buy'
        record['createdAt'] = e['createdAt']
        record['stock_value'] = -e['price'] * e['quantity'] if e['type'] == True else e['price'] * e['quantity']
        record_list.append(record)
    
    return render(request, 'record/record.html',{'record': record_list})

def analysis(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    record_account = sim_models.Owned.objects.filter(user_id=uid).values()
    
    record_value = []
    for e in record_account:
       
        value = {}

        value['stockname'] = stock_models.Stock.objects.get(id= e['stock_id']).symbol

        value['unit'] = e['quantity']
        value['owned_value'] = e['avg_price'] * e['quantity']
        value['current_value'] = stock_models.Stock.objects.get(id= e['stock_id']).price * e['quantity']
        e = value['current_value'] - value['owned_value']
        if e > 0:
            value['profit'] = float(e)
            value['loss'] = 0
        else:
            value['profit'] = 0
            value['loss'] = float(e)

        value['owned_value'] = float(value['owned_value'])
        value['current_value'] = float(value['current_value'])
    
        record_value.append(value)
    account = {}
    
    account['account'] = record_value
    return render(request, 'record/analysis.html', account)
