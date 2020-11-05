from stock import models
import time
import json
import requests
import datetime
from django.utils.timezone import utc

def update_stock():
    token = 'buch32v48v6t51vholng'
    stock_list = models.Stock.objects.all()
    for stock in stock_list:
        # get data
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + stock.symbol + '&token=' + token)

        if quote.status_code != 200:  # fail to get data
            continue

        quote = json.loads(quote.text)  # convert data from json to dict

        if quote['t'] == 0:  # the api return a null dict
            continue

        # store it to the local
        stock.price=float(quote['c']),
        stock.open=float(quote['o']),
        stock.close=float(quote['pc']),
        stock.high=float(quote['h']),
        stock.low=float(quote['l']),
        stock.updateAt=datetime.fromtimestamp(int(quote['t'])).astimezone(utc)

        time.sleep(1)
    stock.save()
