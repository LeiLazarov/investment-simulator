import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.shortcuts import render, redirect

# Create your views here.
from watchlist.models import WatchList


def watchlist(request):
    my_watchlist = WatchList.objects.filter(user=1)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(my_watchlist, 2)
    try:
        page_watchlist = paginator.page(page_number)
    except PageNotAnInteger:
        page_watchlist = paginator.page(1)
    except EmptyPage:
        page_watchlist = paginator.page(paginator.num_pages)
    for stock in page_watchlist:
        # print(stock.symbol)
        stock_quote = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + stock.symbol + '&token=buajtbf48v6ocn3pc8ug')
        company_info = requests.get(
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + stock.symbol + '&token=buajtbf48v6ocn3pc8ug')
        stock.stock_quote = stock_quote.json()
        stock.company_info = company_info.json()
        # print(stock.stock_quote)
        # print(stock_quote.json())
        # print(company_info.json())
        # print(stock.user.username)
        # print(stock.createdAt)
    return render(request, 'watchlist/watchlist.html', {'my_watchlist': page_watchlist})


def watchlist_detail(request, id):
    print(id)
    stock_detail = WatchList.objects.get(pk=id)
    stock_quote = requests.get(
        'https://finnhub.io/api/v1/quote?symbol=' + stock_detail.symbol + '&token=buajtbf48v6ocn3pc8ug')
    company_info = requests.get(
        'https://finnhub.io/api/v1/stock/profile2?symbol=' + stock_detail.symbol + '&token=buajtbf48v6ocn3pc8ug')
    stock_detail.stock_quote = stock_quote.json()
    stock_detail.company_info = company_info.json()

    return render(request, 'watchlist/watchlist_detail.html', {'stock_detail': stock_detail})


def watchlist_delete(request, offset):
    code = offset.upper()
    # delete_id = request.GET.get('delete_id')
    WatchList.objects.filter(symbol=code).delete()
    return redirect('/watchlist/')
