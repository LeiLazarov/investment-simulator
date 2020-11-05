from django.contrib import admin

# Register your models here.
from stock.models import Stock, Detail


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'price', 'open', 'close', 'high', 'low')


admin.site.register(Stock, StockAdmin)


class DetailAdmin(admin.ModelAdmin):
    list_display = ('stock', 'symbol', 'country', 'currency', 'exchange', 'phone')


admin.site.register(Detail, DetailAdmin)

