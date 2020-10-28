from django.contrib import admin


# Register your models here.
from watchlist.models import WatchList


class WatchListAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'user', 'createdAt')


admin.site.register(WatchList, WatchListAdmin)
