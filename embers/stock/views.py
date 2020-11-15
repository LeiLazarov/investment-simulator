import requests
from django.shortcuts import render, redirect
from stock import models
from datetime import datetime, timedelta
from django.utils.timezone import utc
import json
import time
import os
from django.http import HttpResponse

from embers import settings
from stock.models import Stock, Detail, Symbol
from watchlist.models import WatchList, User
from django.db.models import Q

def stock(request, offset):
    try:
        offset = offset.upper() # convert to upper char
        stockItem = getStockQuote(offset)
        detailItem = getStockDetail(offset)
        getCandle(offset)
    except Exception as e:
        return render(request, 'error.html', {'message':e.args[0]})

    return render(request, 'detail.html', {"stock": detailItem, 'price': stockItem})


# get the stock quote from its symbol
def getStockQuote(symbol):
    token = 'buch32v48v6t51vholng'
    # search the local database
    stockFilter = Stock.objects.filter(symbol=symbol)

    if stockFilter.exists(): # local contains
        stockItem = stockFilter.first()
        return stockItem
    else:  # get it from API and store in the local
        # get data
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)

        if quote.status_code != 200:  # fail to get data
            raise Exception('Connect time out!')

        quote = json.loads(quote.text)  # convert data from json to dict

        if quote['t'] == 0:  # the api return a null dict
            raise Exception('No stock found!')
        # store it to the local
        stockItem = Stock.objects.create(
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
def getStockDetail(symbol):
    detailFilter = Detail.objects.filter(symbol=symbol)

    if detailFilter.exists():  # local contains
        return detailFilter.first()
    else:  # get it from API and store in the local
        token = 'buch32v48v6t51vholng'
        # get data of company
        info = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + token)

        if info.status_code != 200:
            raise Exception('Connect time out!')
        # convert company info from json to dict
        info = json.loads(info.text)

        # store company info to local
        stock = models.Stock.objects.get(symbol=symbol)
        if info == {}:
            detailItem = Detail.objects.create(
                stock=stock,
                symbol=symbol
            )
        else:
            detailItem = Detail.objects.create(
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

def getCandle(symbol):
    # store canverted json file
    file_path = settings.MEDIA_ROOT + '\candles\\' + symbol + '.json'
    if not os.path.exists(file_path):
        token = 'buch32v48v6t51vholng'
        # get the candle json file
        nowTime = int(time.time())
        lastTime = nowTime - 2592000  # to last month
        candle = requests.get(
            'https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution=D&from={1}&to={2}&token={3}'.format(symbol,
                                                                                                              lastTime,
                                                                                                              nowTime,
                                                                                                              token))
        if candle.status_code != 200:
            raise Exception('No company info found!')

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

        with open(file_path, 'w') as f:
            json.dump(result, f)


def search(request, offset):
    try:
        offset = offset.upper() # convert to upper char
        stocks_list = []  # 存所有查询到的可能的stocks
        # stock_code = request.POST.get('stock_code').upper()  # 这里的stock_code可能是code也可能是公司名称之类,模糊查
        stock_code = offset
        # 如果这里写symbol=code，不模糊查询的话，只要触发就返回结果了；换句话说，只能拿到一个stock
        stocks = models.Symbol.objects.filter(Q(symbol__contains=stock_code) | Q(cmpname__contains=stock_code))[:9]
        # 已经在数据库里查到stock, 去拿symbol和company_name
        if stocks.exists():
            for one_stock in stocks:
                # 数据库里record拿出来的形式，是model
                stockItem = {}
                quote_res = getStockQuote(one_stock.symbol)

                stockItem['symbol'] = one_stock.symbol
                stockItem['name'] = one_stock.cmpname
                stockItem['price'] = quote_res.price
                stockItem['close'] = quote_res.close
                stockItem['chg'] = quote_res.price - quote_res.close
                stockItem['res'] = "{:.3f}".format((stockItem['chg']) * 100 / stockItem['close'])
                stockItem['date'] = quote_res.updateAt
                stocks_list.append(stockItem)

            return render(request, 'result.html', {'stocks_list': stocks_list})

        else:
            message = "stock might not exist"
            return render(request, 'result.html', {'message': message})

    except Exception as e:
        return render(request, 'error.html', {'message': e.args[0]})

def post_follow(request, sym):
    # 通过stock.html里的“Follow”按钮拿到了company_info.ticker, 通过url传递过来
    try:
        user_id = request.session.get('user_id', '')
        if WatchList.objects.filter(symbol=sym, user=user_id):
            # 该symbol已经被此用户follow，执行“提示”
            message = "The stock is already in your list."
            # return render(request, '/search/%s/' % sym, {'message': message})
            return HttpResponse(json.dumps({'type': 'error', 'message': message}), content_type="application/json")
        else:
            # 该symbol未被此用户follow，执行“添加”
            item_id = User.objects.get(id=user_id)  # WatchList.user是来自User.id的外键，要先实例化外键database
            WatchList(symbol=sym, user=item_id).save()  # 再把外键作为WatchList的键，进行添加save
            return HttpResponse(json.dumps({'type': 'success'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'type': 'error', 'message': e.args[0]}), content_type="application/json")

