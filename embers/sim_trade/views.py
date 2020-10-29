import time

import requests
from django.shortcuts import render, redirect
from sim_trade import models
from datetime import datetime
import json
import datetime
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

        return render(request, 'sim_trade/stock.html', {'stock': stock_quote.json(), 'company_info': company_info.json(),
                                                        'found_stock_flag': found_stock_flag})

def follow_post(request):

    return render(request)

'''
def sim_trade(request):
    if request.method == 'GET':
        # print('get')
        return render(request, 'sim_trade/sim_trade.html')
    elif request.method == 'POST':
        stock_code = request.POST.get('stock_code')
        stock_quote = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + stock_code + '&token=buajtbf48v6ocn3pc8ug')
        company_info = requests.get(
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + stock_code + '&token=buajtbf48v6ocn3pc8ug'
        )

        # stock_candles = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + stock_code
        #                              + '&resolution=D&from=1572651390&to=1572910590&token=buajtbf48v6ocn3pc8ug')
        # print(stock_quote.json())
        stock_time = stock_quote.json()['t']
        stock_time = time.localtime(stock_time)
        stock_time = time.strftime('%Y-%m-%d %H:%M:%S', stock_time)
        # print(company_info.json()['logo'])
        # print(stock_time)
        # print(company_info.json())
        # print(stock_candles.json())
        return render(request, 'sim_trade/stock.html', {'stock': stock_quote.json(), 'company_info': company_info.json(),
                                                        'stock_time': stock_time})

'''
def detail(request):
    stock = models.Detail.objects.get(pk=1)
    # json_data = stock.candle
    # result = []
    # for i in range(len(json_data['t'])):
    #     temp = []
    #     date = datetime.datetime.utcfromtimestamp(json_data['t'][0]).strftime("%Y/%m/%d")
    #     temp.append(date)
    #     temp.append(json_data['o'][i])
    #     temp.append(json_data['h'][i])
    #     temp.append(json_data['l'][i])
    #     temp.append(json_data['c'][i])
    #     temp.append(json_data['v'][i])
    #     result.append(temp)
    # json_data = json.dumps(result)
    return render(request, 'sim_trade/detail.html',{"stock": stock})
