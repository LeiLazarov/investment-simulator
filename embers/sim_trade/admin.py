from django.contrib import admin

# Register your models here.
from sim_trade.models import Owned, Record


class OwnedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stock', 'quantity', 'avg_price', 'min_price', 'max_price')


admin.site.register(Owned, OwnedAdmin)


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stock', 'quantity', 'price', 'type')


admin.site.register(Record, RecordAdmin)
