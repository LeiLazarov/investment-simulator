from django.shortcuts import render


# Create your views here.
def sim_trade(request):
    return render(request, 'sim_trade/sim_trade.html')
