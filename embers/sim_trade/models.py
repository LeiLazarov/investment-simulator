from django.db import models
# from watchlist.models import WatchList


class Owned(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('login.User', on_delete=models.CASCADE)
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    avg_price = models.DecimalField(max_digits=6,decimal_places=2)
    min_price = models.DecimalField(max_digits=6,decimal_places=2)
    max_price = models.DecimalField(max_digits=6,decimal_places=2)


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('login.User', on_delete=models.CASCADE)
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.BooleanField() # buy: false, sell: true
    createdAt = models.DateTimeField(auto_now_add=True)
