from django.shortcuts import render
from sim_trade import models
from datetime import datetime
import json
import datetime
# Create your views here.

def sim_trade(request):
    return render(request, 'sim_trade/sim_trade.html')

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
