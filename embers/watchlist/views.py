import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.db.models import Q


# Create your views here.
from watchlist.models import WatchList
from stock.models import Stock

def watchlist(request):
    uid = request.session.get('user_id', '')
    if not uid:
        return redirect("/login/")
    watchlist_account = WatchList.objects.filter(user_id=uid).values()
    watchlist_list = []
# Retrieve stock information from "stock.model"
    for e in watchlist_account:
        stockItem = Stock.objects.get(symbol=e['symbol'])
        WL = {}
        WL['id'] = e['id']
        WL['symbol'] = e['symbol']
        WL['c'] = stockItem.price
        WL['pc'] = stockItem.close
        WL['chg'] = stockItem.price - stockItem.close
# Percentage Change = (current unit price- previous day's unit price) / previous day's unit price
        WL['res'] = "{:.3f}".format( WL['chg'] * 100 / WL['pc'])
        WL['upd'] = Stock.objects.get(symbol=e['symbol']).updateAt
        WL['createdAt'] = e['createdAt']
        watchlist_list.append(WL)
    
    return render(request, 'watchlist/watchlist.html', {'my_watchlist': watchlist_list})

# remove function of remove bottom
def delete(request):
    uid = request.session.get('user_id', '')
    delete_id = request.GET.get('delete_id')
    code = delete_id.upper()
    WatchList.objects.filter(Q(symbol=code),Q(user_id=uid)).delete()
    return redirect('/watchlist/')



