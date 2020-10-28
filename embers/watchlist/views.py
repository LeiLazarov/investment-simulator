import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.shortcuts import render


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
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + stock.symbol + '&token=buajtbf48v6ocn3pc8ug'
        )
        stock.stock_quote = stock_quote.json()
        stock.company_info = company_info.json()
        # print(stock.stock_quote)
        # print(stock_quote.json())
        # print(company_info.json())
        # print(stock.user.username)
        # print(stock.createdAt)
    return render(request, 'watchlist/watchlist.html', {'my_watchlist': page_watchlist})



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
