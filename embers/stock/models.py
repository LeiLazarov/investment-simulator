from django.db import models
import datetime

class Stock(models.Model):
    id = models.AutoField(primary_key=True)  # The unique id for our project
    symbol = models.CharField(null=False, max_length=16)  # Company symbol/ticker as used on the listed exchange.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    open = models.DecimalField(max_digits=6, decimal_places=2)
    close = models.DecimalField(max_digits=6, decimal_places=2)
    high = models.DecimalField(max_digits=6, decimal_places=2)
    low = models.DecimalField(max_digits=6, decimal_places=2)
    updateAt = models.DateTimeField()  # The last update date

    def __str__(self):
        return 'Stock_' + self.symbol


class Detail(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE,primary_key=True)  # The unique id for our project
    symbol = models.CharField(null=False, max_length=16)  # Company symbol/ticker as used on the listed exchange.
    country = models.CharField(null=False, max_length=8, default='US')  # Country of company's headquarter
    currency = models.CharField(null=False, max_length=8, default='USD')  # Currency used in company filings
    exchange= models.CharField(null=False, max_length=32, default='-')  # Listed exchange
    ipo = models.DateField(null=False, default=datetime.date.today)
    marketCapitalization = models.IntegerField(null=False,default=0)  # Market Capitalization
    phone = models.CharField(null=False, max_length=32, default='-')  # Company phone number
    shareOutstanding = models.FloatField(default=0.0)  # Number of oustanding shares
    cmpname = models.CharField(null=False, max_length=32, default='No data')  # Company name
    weburl = models.URLField(max_length=200, default='-')  # Company website
    logo = models.CharField(max_length=256, default='')  # Logo image
    industry = models.CharField(null=False, max_length=32, default='-')  # Industry classification
    updateAt = models.DateTimeField(auto_now_add=True)  # The last update date

    def __str__(self):
        return 'Detail_' + self.symbol

class Symbol(models.Model):
    id = models.AutoField(primary_key=True)  # The unique id for our project
    symbol = models.CharField(null=False, max_length=16)  # Company symbol/ticker as used on the listed exchange.
    cmpname = models.CharField(null=False, max_length=32)  # Company name

    def __str__(self):
        return 'Symbol_' + self.symbol


