import requests
from django.shortcuts import render, redirect
from django.db import models
from stock.models import Stock
from login.models import User
from watchlist.models import WatchList
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from decimal import *
from stock.views import getStockQuote
import datetime


# Create your views here.

# Yiren 的 sim_trade/views在下面

def sim_trade(request):
    if request.method == 'GET':
        not_found_msg = None
        return render(request, 'sim_trade/sim_trade.html', {'not_found_msg': not_found_msg})

    elif request.method == 'POST':
        stock_code = request.POST.get('stock_code').upper()
        stock_quote = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + stock_code + '&token=buajtbf48v6ocn3pc8ug')
        company_info = requests.get(
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + stock_code + '&token=buajtbf48v6ocn3pc8ug'
        )

        # stock_candles = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + stock_code
        #                              + '&resolution=D&from=1572651390&to=1572910590&token=buajtbf48v6ocn3pc8ug')
        # print(stock_quote.json())
        # print(company_info.json())

        if len(company_info.json()) == 0:
            not_found_msg = "Not found stock!"
            return render(request, 'sim_trade/sim_trade.html', {'not_found_msg': not_found_msg})

    return render(request, 'sim_trade/stock.html', {'stock': stock_quote.json(), 'company_info': company_info.json()})


def post_follow(request, sym):
    # print(sym)
    # 通过stock.html里的“Follow”按钮拿到了company_info.ticker, 通过url传递过来
    if request.method == 'POST':
        if WatchList.objects.filter(symbol=sym, user=1):
            # 该symbol已经被此用户follow，执行“提示”
            # models.WatchList.objects.filter(user=1, symbol=sym).delete()
            return HttpResponse("already  in your list")# 为什么already和in之间有两个空格才显示一个空格
        else:
            # 该symbol未被此用户follow，执行“添加”
            item_id = User.objects.get(id=1)# WatchList.user是来自User.id的外键，要先实例化外键database
            WatchList(symbol=sym, user=item_id).save()# 再把外键作为WatchList的键，进行添加save
            return HttpResponse("successfully  followed")

    else:
        raise Exception


def table(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    # statistics part
    stats = refreshStat(uid)
    acc = {'a': "${:,}".format(stats[0]), 'c': "${:,}".format(stats[1])
        , 's': "${:,}".format(stats[2]), 'e': "${:,}".format(stats[3])
        , 'cv':str(stats[1]),'sv':str(stats[2])}

    # owned stock part
    owned_list = models.Owned.objects.filter(user_id=uid)

    return render(request, 'sim_trade/table.html', {'acc': acc, 'owned_list':owned_list})


def checkStock(request, offset):
    try:
        stockItem = getStockQuote(request, offset.upper())
        if stockItem:
            res = json.loads(serialize('json', [stockItem])[1:-1])['fields']
            res['name']=stockItem.detail.cmpname
            res['type']='success'
            return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse({'type':'error'}, content_type="application/json")
    return HttpResponse({'type':'error'}, content_type="application/json")


def sellCheckStock(request, offset):
    uid = request.session.get('user_id', '')
    try:
        stockItem = getStockQuote(request, offset.upper())
        if stockItem:
            ownStock = models.Owned.objects.get(user_id=uid,stock=stockItem)
            res = json.loads(serialize('json', [stockItem])[1:-1])['fields']
            res['volume'] = ownStock.quantity
            res['name'] = stockItem.detail.cmpname
            res['type']='success'
            return HttpResponse(json.dumps(res), content_type="application/json")
    except Exception as e:
        return HttpResponse({'type':'error'}, content_type="application/json")
    return HttpResponse({'type':'error'}, content_type="application/json")


def getOwned(request):
    try:
        uid = request.session.get('user_id', '')
        queryset = models.Owned.objects.filter(user_id=uid)
        res = json.loads(serialize('json', queryset))
        data = []
        for row in res:
            row['fields']['values']="${:,}".format(int(row['fields']['quantity'])*Decimal(row['fields']['avg_price']))
            row['fields']['id'] = row['pk']
            row['fields']['symbol'] = Stock.objects.get(pk=row['fields']['stock']).symbol
            data.append(row['fields'])
    except Exception as e:
        return HttpResponse({'type':'error'}, content_type="application/json")
    return HttpResponse(json.dumps(data), content_type="application/json")


def buy_stock(request):
    ret = {'type': 'fail', 'message': ''}
    data = json.loads(request.body)
    s_symbol = data['symbol']
    s_price = Decimal(data['price']).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    s_num = int(data['number'])
    uid = request.session.get('user_id', '')
    try:
        user = User.objects.get(id=uid)
        stock = Stock.objects.get(symbol=s_symbol)
        own_stock = models.Owned.objects.filter(user=user, stock=stock)
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
            models.Owned.objects.create(
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

    except Exception as e:
        return HttpResponse(json.dumps(ret), content_type="application/json")
    ret['type'] = 'success'
    return HttpResponse(json.dumps(ret), content_type="application/json")


def sell_stock(request):
    ret = {'type': 'fail', 'message': ''}
    data = json.loads(request.body)
    s_symbol = data['symbol']
    s_price = Decimal(data['price']).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    s_num = int(data['number'])
    uid = request.session.get('user_id', '')
    try:
        user = User.objects.get(id=uid)
        stock = Stock.objects.get(symbol=s_symbol)
        own_stock = models.Owned.objects.filter(user=user, stock=stock)
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

    except Exception as e:
        return HttpResponse(json.dumps(ret), content_type="application/json")
    ret['type'] = 'success'
    return HttpResponse(json.dumps(ret), content_type="application/json")


def refreshStat(uid):
    user = User.objects.get(pk=uid)
    # modify the statistics
    ownStocks =models.Owned.objects.filter(user=user)
    stockValue = Decimal(0)
    for ss in ownStocks:
        stockValue+= ss.quantity * ss.stock.price

    # account value, cash, stock value, earning
    return [stockValue+user.cash, user.cash, stockValue, stockValue+user.cash-user.init]

