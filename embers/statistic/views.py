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
    #check the user_id
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    
    #get the record according to uid
    record_account = sim_models.Record.objects.filter(user_id=uid).values()
    record_list = []
    
    #change the record data to fit the table 
    for i in range(len(record_account)):
        record = {}
        record['id'] = i + 1
        record['stockname'] = stock_models.Stock.objects.get(id= record_account[i]['stock_id']).symbol
        record['quantity'] = record_account[i]['quantity']
        record['price'] = record_account[i]['price']
        record['type'] = 'sell' if record_account[i]['type'] == True else 'buy'
        record['createdAt'] = record_account[i]['createdAt']
        record['stock_value'] = -record_account[i]['price'] * record_account[i]['quantity'] if record_account[i]['type'] == True else record_account[i]['price'] * record_account[i]['quantity']
        record_list.append(record)
    
    return render(request, 'record/record.html',{'record': record_list})

def analysis(request):
    #check uid
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    
    #get the owned data 
    record_account = sim_models.Owned.objects.filter(user_id=uid).values()

    #mark the total paid value 
    total_value = 0
    record_value = []

    #change the data to json form
    for e in record_account:     
        value = {}
        value['stockname'] = stock_models.Stock.objects.get(id= e['stock_id']).symbol      
        value['unit'] = e['quantity']
        value['owned_value'] = e['avg_price'] * e['quantity'] # total paid value
        value['current_value'] = stock_models.Stock.objects.get(id= e['stock_id']).price * e['quantity'] #current value
       
        value['owned_value'] = float(value['owned_value'])
        value['current_value'] = float(value['current_value'])

        e = value['current_value'] - value['owned_value']
        if e > 0:
            value['profit'] = e
        else:
            value['loss'] = e

        
        #calculate the total paid value
        total_value +=  value['owned_value']
        record_value.append(value)

    #set the threshold of data
    value_thr = total_value * 0.01

    return render(request, 'record/analysis.html', {'account': record_value, 'value_thr': value_thr})
