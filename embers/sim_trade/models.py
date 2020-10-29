from django.db import models
from django.core.files.storage import FileSystemStorage

class Owned(models.Model):
    ownedID = models.AutoField(primary_key=True)
    userID = models.CharField(max_length=64)
    stockID = models.CharField(max_length=64)
    quantity = models.IntegerField()
    avg_price = models.DecimalField(max_digits=6,decimal_places=2)
    min_price = models.DecimalField(max_digits=6,decimal_places=2)
    max_price = models.DecimalField(max_digits=6,decimal_places=2)

class Record(models.Model):
    recordID = models.AutoField(primary_key=True)
    userID = models.CharField(max_length=64)
    stockID = models.CharField(max_length=64)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.BooleanField() # buy: false, sell: true
    createdAt = models.DateTimeField(auto_now_add=True)