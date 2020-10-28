from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location='/media/logos')

# Create your models here.
class Detail(models.Model):
    stockID = models.IntegerField(unique=True, primary_key=True) # The unique id for our project
    symbol = models.CharField(null=False, max_length=128) # Company symbol/ticker as used on the listed exchange.
    country = models.CharField(null=False, max_length=8) # Country of company's headquarter
    currency = models.CharField(null=False, max_length=8) # Currency used in company filings
    exchange= models.CharField(null=False, max_length=32) # Listed exchange
    phone = models.CharField()
    ipo = models.DateTimeField()
    marketCapitalization = models.IntegerField() # Market Capitalization
    phone = models.CharField(null=False, max_length=32) # Company phone number
    shareOutstanding = models.FloatField()# Number of oustanding shares
    cmpname = models.CharField(null=False, max_length=32) # Company name
    weburl = models.URLField(max_length=200) # Company website
    candle = models.JSONField() # JSON data for this stock candle chart
    logo = models.FileField(upload_to='logos/',default='logos/empty.png',storage=fs) # Logo image
    industry = models.CharField(null=False, max_length=32) # Industry classification
    updateAt = models.DateTimeField(auto_now_add=True) # The last update date

class Owned(models.Model):
    ownedID = models.AutoField(primary_key=True)
    userID = models.CharField(max_length=64)
    stockID = models.CharField(max_length=64)
    quantity = models.IntegerField()
    avg_price = models.FloatField()
    min_price = models.FloatField()
    max_price = models.FloatField()