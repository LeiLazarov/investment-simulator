import requests
from django.shortcuts import render, redirect
from sim_trade import models
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from decimal import *


# Create your views here.

# Yiren 的 sim_trade/views在下面

def sim_trade(request):
    if request.method == 'GET':
        return render(request, 'sim_trade/sim_trade.html')

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
            found_stock_flag = 0
            return render(request, 'sim_trade/not_found_stock.html')
        else:
            found_stock_flag = 1

        return render(request, 'sim_trade/stock.html',
                      {'stock': stock_quote.json(), 'company_info': company_info.json(),
                       'found_stock_flag': found_stock_flag})


def follow_post(request):
    return render(request)


def table(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    return render(request, 'sim_trade/table.html')


def getOwned(request):
    queryset = models.Owned.objects.filter(userID=1)
    fields = ('ownedID', 'stockID', 'quantity', 'avg_price', 'min_price', 'max_price')
    res = json.loads(serialize('json', queryset, fields=fields))
    data = []
    for row in res:
        data.append(row['fields'])
    return HttpResponse(json.dumps(data), content_type="application/json")


def buy_stock(request):
    ret = {'type': 'fail', 'message': ''}
    data = json.loads(request.body)
    s_symbol = data['symbol']
    s_price = Decimal(data['price']).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    s_num = int(data['number'])
    uid = request.session.get('user_id', '')
    try:
        record = models.Owned.objects.filter(userID=uid, stockID=s_symbol)
        if record.exists():
            element = record.first()
            num = element.quantity + s_num
            avg = ((element.quantity * element.avg_price + s_num * s_price) / num).quantize(Decimal('.00'),
                                                                                            rounding=ROUND_DOWN)
            element.quantity = num
            element.avg_price = avg
            if s_price > element.max_price:
                element.max_price = s_price
            elif s_price < element.min_price:
                element.min_price = s_price
            else:
                element.save()
        else:
            models.Owned.objects.create(
                userID=uid,
                stockID=s_symbol,
                quantity=s_num,
                avg_price=s_price,
                min_price=s_price,
                max_price=s_price,
            )
        models.Record.objects.create(
            userID=uid,
            stockID=s_symbol,
            quantity=s_num,
            price=s_price,
            type=False  # buy: false, sell: true
        )
    except Exception as e:
        return HttpResponse(json.dumps(ret), content_type="application/json")
    ret['type'] = 'success'
    return HttpResponse(json.dumps(ret), content_type="application/json")
