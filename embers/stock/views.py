import requests
from django.shortcuts import render, redirect
from stock import models
from datetime import datetime
import json
import time
from django.http import Http404


def stock(request, offset):
    try:
        stockItem = models.Stock.objects.get(symbol=offset)
    except Exception as e:
        isAdd = getDataFromAPI(offset)
        if isAdd:
            stockItem = models.Stock.objects.get(symbol=offset)
            detailItem = models.Detail.objects.get(symbol=offset)
            return render(request, 'detail.html', {"stock": detailItem, 'price': stockItem})
        return Http404('Cannot found stock!') # should design a error page
    detailItem = models.Detail.objects.get(symbol=offset)
    return render(request, 'detail.html', {"stock": detailItem, 'price': stockItem})


# implement add the stock to database
def getDataFromAPI(symbol):
    token = 'buch32v48v6t51vholng'
    quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)

    if quote.status_code != 200:
        return False
    quote = json.loads(quote.text)

    if quote['t'] == '0':
        return False

    info = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + token)
    if info.status_code != 200:
        return False
    info = json.loads(info.text)

    nowTime = int(time.time())
    lastTime = nowTime - 31622400
    candle = requests.get(
        'https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution=D&from={1}&to={2}&token={3}'.format(symbol,
                                                                                                          lastTime,
                                                                                                          nowTime,
                                                                                                          token))

    if candle.status_code != 200:
        return False
    candle = json.loads(candle.text)
    result = {'categoryData': [], 'values': [], 'volumes': []}
    for i in range(len(candle['t'])):
        date = datetime.utcfromtimestamp(candle['t'][0]).strftime("%Y/%m/%d")
        values = []
        values.append(round(candle['o'][i],2))
        values.append(round(candle['c'][i],2))
        values.append(round(candle['l'][i],2))
        values.append(round(candle['h'][i],2))
        values.append(candle['v'][i])
        result['categoryData'].append(date)
        result['values'].append(values)
        volumes = []
        volumes.append(i)
        volumes.append(candle['v'][i])
        if candle['o'][i]>candle['c'][i]:
            volumes.append(1)
        else:
            volumes.append(-1)
        result['volumes'].append(volumes)
    url = './media/candles/' + symbol + '.json'
    with open(url, 'w') as f:
        json.dump(result, f)
    stockItem = models.Stock.objects.create(
        symbol=symbol,
        price=float(quote['c']),
        open=float(quote['o']),
        close=float(quote['pc']),
        high=float(quote['h']),
        low=float(quote['l']),
        updateAt=datetime.fromtimestamp(int(quote['t']))
    )
    models.Detail.objects.create(
        stockID=stockItem.stockID,
        symbol=symbol,
        country=info['country'],
        currency=info['currency'],
        exchange=info['exchange'],
        phone=info['phone'],
        ipo=info['ipo'],
        marketCapitalization=info['marketCapitalization'],
        shareOutstanding=info['shareOutstanding'],
        cmpname=info['name'],
        weburl=info['weburl'],
        logo=info['logo'],
        industry=info['finnhubIndustry'],
    )

    return True
