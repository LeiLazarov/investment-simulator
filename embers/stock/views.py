import requests
from django.shortcuts import render, redirect
from stock import models
from datetime import datetime, timedelta
from django.utils.timezone import utc
import json
import time
from django.http import Http404

def stock(request, offset):
    try:
        offset = offset.upper() # convert to upper char
        stockItem = getStockQuote(request, offset)
        detailItem = getStockDetail(request, offset)
    except Exception as e:
        return render(request, 'detail.html', {'error':True})

    return render(request, 'detail.html', {"stock": detailItem, 'price': stockItem})


# get the stock quote from its symbol
def getStockQuote(request, symbol):
    token = 'buch32v48v6t51vholng'
    # search the local database
    stockFilter = models.Stock.objects.filter(symbol=symbol)

    if stockFilter.exists(): # local contains
        stockItem = stockFilter.first()
        # if the update time > 10 min, update it from API
        now = datetime.utcnow().replace(tzinfo=utc)
        u_time = stockItem.updateAt
        if u_time + timedelta(minutes=10) < now:
            # get data
            quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)

            if quote.status_code != 200:  # fail to get data
                return stockItem

            quote = json.loads(quote.text)  # convert data from json to dict

            if quote['t'] == 0:  # the api return a null dict
                return stockItem

            if quote['t'] == int(time.mktime(stockItem.updateAt.timetuple())): # no need to update
                return stockItem

            stockItem.price=quote['c']
            stockItem.open=quote['o']
            stockItem.close=quote['pc']
            stockItem.high=quote['h']
            stockItem.low=quote['l']
            stockItem.updateAt = datetime.fromtimestamp(int(quote['t'])).replace(tzinfo=None)
            stockItem.save()

        return stockItem
    else: # get it from API and store in the local
        # get data
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)

        if quote.status_code != 200: # fail to get data
            raise Exception

        quote = json.loads(quote.text) # convert data from json to dict

        if quote['t'] == 0: # the api return a null dict
            raise Exception
        # store it to the local
        stockItem = models.Stock.objects.create(
            symbol=symbol,
            price=float(quote['c']),
            open=float(quote['o']),
            close=float(quote['pc']),
            high=float(quote['h']),
            low=float(quote['l']),
            updateAt=datetime.fromtimestamp(int(quote['t'])).astimezone(utc)
        )
        return stockItem

# similar to get stock, it gets stock detail from its symbol
def getStockDetail(request,symbol):
    detailFilter = models.Detail.objects.filter(symbol=symbol)

    if detailFilter.exists():  # local contains
        return detailFilter.first()
    else:  # get it from API and store in the local
        token = 'buch32v48v6t51vholng'
        # get data of company
        info = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + token)

        if info.status_code != 200:
            raise Exception
        # convert company info from json to dict
        info = json.loads(info.text)
        # get the candle json file
        nowTime = int(time.time())
        lastTime = nowTime - 31622400
        candle = requests.get('https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution=D&from={1}&to={2}&token={3}'.format(symbol,lastTime,nowTime,token))

        if candle.status_code != 200:
            raise Exception
        # convert candle from json to dict
        candle = json.loads(candle.text)
        # convert candle structure to chart form
        result = {'categoryData': [], 'values': [], 'volumes': []}
        for i in range(len(candle['t'])):
            date = datetime.utcfromtimestamp(candle['t'][i]).strftime("%Y/%m/%d")
            values = []
            values.append(round(candle['o'][i], 2))
            values.append(round(candle['c'][i], 2))
            values.append(round(candle['l'][i], 2))
            values.append(round(candle['h'][i], 2))
            values.append(candle['v'][i])
            result['categoryData'].append(date)
            result['values'].append(values)
            volumes = []
            volumes.append(i)
            volumes.append(candle['v'][i])
            if candle['o'][i] > candle['c'][i]:
                volumes.append(1)
            else:
                volumes.append(-1)
            result['volumes'].append(volumes)
        # store canverted json file
        url = './media/candles/' + symbol + '.json'
        with open(url, 'w') as f:
            json.dump(result, f)
        # store company info to local
        stock = models.Stock.objects.get(symbol=symbol)
        detailItem = models.Detail.objects.create(
            stock=stock,
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
        return detailItem