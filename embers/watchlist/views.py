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

    for e in watchlist_account:
        WL = {}
        WL['id'] = e['id']
        WL['symbol'] = e['symbol']
        WL['c'] = Stock.objects.get(symbol=e['symbol']).price
        WL['pc'] = Stock.objects.get(symbol=e['symbol']).close
        WL['chg'] = WL['c'] - WL['pc']
        WL['res'] = "{:.3f}".format((WL['c'] - WL['pc']) * 100 / WL['pc'])
        WL['upd'] = Stock.objects.get(symbol=e['symbol']).updateAt
        WL['createdAt'] = e['createdAt']
        watchlist_list.append(WL)
    
    return render(request, 'watchlist/watchlist.html', {'my_watchlist': watchlist_list})



def delete(request):
    uid = request.session.get('user_id', '')
    delete_id = request.GET.get('delete_id')
    code = delete_id.upper()
    WatchList.objects.filter(Q(symbol=code),Q(user_id=uid)).delete()
    return redirect('/watchlist/')


# def reviews(request):
#     review_list = Review.objects.all()
#     page_number = request.GET.get('page', 1)
#     paginator = Paginator(review_list, 2)
#     try:
#         page_reviews = paginator.page(page_number)
#     except PageNotAnInteger:
#         page_reviews = paginator.page(1)
#     except EmptyPage:
#         page_reviews = paginator.page(paginator.num_pages)
#
#     return render(request, 'reviews.html', {'page_reviews': page_reviews})
#
# def watchlist_detail(request, id):
#      stock_detail = WatchList.objects.get(pk=id)
#      stock_quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + stock_detail.symbol + '&token=buajtbf48v6ocn3pc8ug')
#      company_info = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol=' + stock_detail.symbol + '&token=buajtbf48v6ocn3pc8ug')
#      stock_detail.stock_quote = stock_quote.json()
#      stock_detail.company_info = company_info.json()
#      return render(request, 'watchlist/watchlist_detail.html', {'stock_detail': stock_detail})

