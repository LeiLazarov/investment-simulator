import requests
from django.shortcuts import render
from statistic import models
import json
from django.http import HttpResponse
from django.core.serializers import serialize

def table(request):
    return render(request, 'sim_trade/table.html')

def account_record(request):
    #uid = request.session.get('user_id', '')
    uid = 1
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
    uid = 1
    record_account = sim_models.Owned.objects.filter(user_id=uid).values()
    record_unit = []
    record_value = []
    for e in record_account:
        unit = {}
        value = {}

        unit['name'] = stock_models.Stock.objects.get(id= e['stock_id']).symbol
        value['stockname'] = stock_models.Stock.objects.get(id= e['stock_id']).symbol

        unit['value'] = e['quantity']
        value['owned_value'] = float(e['avg_price'] * e['quantity'])
        value['current_value'] = float(stock_models.Stock.objects.get(id= e['stock_id']).price * e['quantity'])
        record_unit.append(unit)
        record_value.append(value)
    
    account = {}
    account['unit'] = record_unit
    account['value'] = record_value
    return render(request, 'record/analysis.html', {'account': account})