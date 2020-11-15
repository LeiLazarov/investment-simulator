import requests
from django.shortcuts import render, redirect
from django.db import models
from stock.models import Stock, Symbol
from login.models import User
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from decimal import *
from stock.views import getStockQuote
import datetime
from sim_trade.models import Owned, Record


# this function return the page of simtrade
def table(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    # statistics part
    stats = refreshStat(uid)
    acc = {'a': "${:,}".format(stats[0]), 'c': "${:,}".format(stats[1])
        , 's': "${:,}".format(stats[2]), 'e': "${:,}".format(stats[3])
        , 'cv':str(stats[1]),'sv':str(stats[2]),'ev':str(stats[3])}

    # owned stock part
    owned_list = Owned.objects.filter(user_id=uid)

    return render(request, 'sim_trade/table.html', {'acc': acc, 'owned_list':owned_list})


# this function for check input stock code is valid
def checkStock(request, offset):
    try:
        # find stock quote from API and local database
        stockItem = getStockQuote(offset.upper())
        if stockItem:
            res = json.loads(serialize('json', [stockItem])[1:-1])['fields']
            res['name']=Symbol.objects.get(symbol=stockItem.symbol).cmpname
            res['type']='success'
            return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'type':'error', 'message': e.args[0]}), content_type="application/json")
    return HttpResponse(json.dumps({'type':'error'}), content_type="application/json")


# similar to checkStock() but it for sell process
def sellCheckStock(request, offset):
    uid = request.session.get('user_id', '')
    try:
        stockItem = getStockQuote(offset.upper())
        if stockItem:
            ownStock = Owned.objects.get(user_id=uid,stock=stockItem)
            res = json.loads(serialize('json', [stockItem])[1:-1])['fields']
            res['volume'] = ownStock.quantity
            res['name'] = Symbol.objects.get(symbol=stockItem.symbol).cmpname
            res['avgp'] = float(ownStock.avg_price)
            res['type']='success'
            return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'type':'error', 'message': e.args[0]}), content_type="application/json")
    return HttpResponse(json.dumps({'type':'error'}), content_type="application/json")


# get the list of owned stocks
def getOwned(request):
    try:
        uid = request.session.get('user_id', '')
        queryset = Owned.objects.filter(user_id=uid)
        res = json.loads(serialize('json', queryset))
        data = []
        for row in res:
            row['fields']['values']="${:,}".format(int(row['fields']['quantity'])*Decimal(row['fields']['avg_price']))
            row['fields']['id'] = row['pk']
            row['fields']['symbol'] = Stock.objects.get(pk=row['fields']['stock']).symbol
            data.append(row['fields'])
    except Exception as e:
        return HttpResponse(json.dumps({'type':'error', 'message': e.args[0]}), content_type="application/json")
    return HttpResponse(json.dumps(data), content_type="application/json")


# process the submitted but order
def buy_stock(request):
    ret = {'type': 'error', 'message': ''}
    data = json.loads(request.body)
    s_symbol = data['symbol'].upper()
    s_price = Decimal(data['price']).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    s_num = int(data['number'])
    uid = request.session.get('user_id', '')
    try:
        user = User.objects.get(id=uid)
        stock = Stock.objects.get(symbol=s_symbol)
        own_stock = Owned.objects.filter(user=user, stock=stock)
        if own_stock.exists():
            # modify the value of holding stock
            element = own_stock.first()
            num = element.quantity + s_num
            avg = ((element.quantity * element.avg_price + s_num * s_price) / num).quantize(Decimal('.00'),
                                                                                            rounding=ROUND_DOWN)
            element.quantity = num
            element.avg_price = avg
            if s_price > element.max_price:
                element.max_price = s_price
            elif s_price < element.min_price:
                element.min_price = s_price
            element.save()
        else:
            stock = Stock.objects.get(symbol=s_symbol)
            # add this stock to owned table
            Owned.objects.create(
                user=user,
                stock=stock,
                quantity=s_num,
                avg_price=s_price,
                min_price=s_price,
                max_price=s_price,
            )
        # reduce cash
        user.cash -=s_price*s_num
        user.save()

        # record this to list
        Record.objects.create(
            user=user,
            stock=stock,
            quantity=s_num,
            price=s_price,
            type=False  # buy: false, sell: true
        )

    except Exception as e:
        return HttpResponse(json.dumps({'type': 'error', 'message': e.args[0]}), content_type="application/json")
    ret['type'] = 'success'
    return HttpResponse(json.dumps(ret), content_type="application/json")


# process the submitted sell order
def sell_stock(request):
    ret = {'type': 'error', 'message': ''}
    data = json.loads(request.body)
    s_symbol = data['symbol']
    s_price = Decimal(data['price']).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    s_num = int(data['number'])
    uid = request.session.get('user_id', '')
    try:
        user = User.objects.get(id=uid)
        stock = Stock.objects.get(symbol=s_symbol)
        own_stock = Owned.objects.filter(user=user, stock=stock)
        if own_stock.exists():
            # modify the value of holding stock
            element = own_stock.first()
            num = element.quantity - s_num
            if num == 0:
                own_stock.delete()
            else:
                element.quantity = num
                element.save()
        else:
            raise Exception
        # increase cash
        user.cash +=s_price*s_num
        user.save()

        # record this to list
        Record.objects.create(
            user=user,
            stock=stock,
            quantity=s_num,
            price=s_price,
            type=True  # buy: false, sell: true
        )

    except Exception as e:
        return HttpResponse(json.dumps({'type':'error', 'message': e.args[0]}), content_type="application/json")
    ret['type'] = 'success'
    return HttpResponse(json.dumps(ret), content_type="application/json")


# tool function for calculating statistic
def refreshStat(uid):
    user = User.objects.get(pk=uid)
    # modify the statistics
    ownStocks = Owned.objects.filter(user=user)
    stockValue = Decimal(0)
    for ss in ownStocks:
        stockValue+= ss.quantity * ss.stock.price

    # [account value, cash, stock value, earning]
    return [stockValue+user.cash, user.cash, stockValue, stockValue+user.cash-user.init]


