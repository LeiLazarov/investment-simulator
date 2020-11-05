from django.shortcuts import render

from sim_trade.models import Record, Owned
from stock.models import Stock


def table(request):
    return render(request, 'sim_trade/table.html')


def account_record(request):
    # uid = request.session.get('user_id', '')
    uid = 1
    record_account = Record.objects.filter(user_id=uid).values()
    record_list = []
    
    for e in record_account:
        record = {}
        record['id'] = e['id']
        record['stockname'] = Stock.objects.get(id= e['stock_id']).symbol
        record['quantity'] = e['quantity']
        record['price'] = e['price']
        record['type'] = 'sell' if e['type'] == True else 'buy'
        record['createdAt'] = e['createdAt']
        record['stock_value'] = -e['price'] * e['quantity'] if e['type'] == True else e['price'] * e['quantity']
        record_list.append(record)
    
    return render(request, 'record/record.html',{'record': record_list})


def analysis(request):
    uid = 1
    record_account = Owned.objects.filter(user_id=uid).values()
    record_unit = []
    record_value = []
    for e in record_account:
        unit = {}
        value = {}

        unit['name'] = Stock.objects.get(id= e['stock_id']).symbol
        value['stockname'] = Stock.objects.get(id= e['stock_id']).symbol

        unit['value'] = e['quantity']
        value['owned_value'] = float(e['avg_price'] * e['quantity'])
        value['current_value'] = float(Stock.objects.get(id= e['stock_id']).price * e['quantity'])
        record_unit.append(unit)
        record_value.append(value)
    
    account = {}
    account['unit'] = record_unit
    account['value'] = record_value
    return render(request, 'record/analysis.html', {'account': account})
