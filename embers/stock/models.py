from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True) # The unique id for our project
    symbol = models.CharField(null=False, max_length=16) # Company symbol/ticker as used on the listed exchange.
    price = models.DecimalField(max_digits=6,decimal_places=2)
    open = models.DecimalField(max_digits=6,decimal_places=2)
    close = models.DecimalField(max_digits=6,decimal_places=2)
    high = models.DecimalField(max_digits=6,decimal_places=2)
    low = models.DecimalField(max_digits=6,decimal_places=2)
    updateAt = models.DateTimeField() # The last update date

class Detail(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE,primary_key=True) # The unique id for our project
    symbol = models.CharField(null=False, max_length=16) # Company symbol/ticker as used on the listed exchange.
    country = models.CharField(null=False, max_length=8) # Country of company's headquarter
    currency = models.CharField(null=False, max_length=8) # Currency used in company filings
    exchange= models.CharField(null=False, max_length=32) # Listed exchange
    phone = models.CharField(null=False, max_length=20)
    ipo = models.DateField()
    marketCapitalization = models.IntegerField() # Market Capitalization
    phone = models.CharField(null=False, max_length=32) # Company phone number
    shareOutstanding = models.FloatField()# Number of oustanding shares
    cmpname = models.CharField(null=False, max_length=32) # Company name
    weburl = models.URLField(max_length=200) # Company website
    logo = models.CharField(max_length=256, default='') # Logo image
    industry = models.CharField(null=False, max_length=32) # Industry classification
    updateAt = models.DateTimeField(auto_now_add=True) # The last update date
