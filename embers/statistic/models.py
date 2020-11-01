from django.db import models

class Statistic(models.Model):
    userID = models.IntegerField(primary_key=True)
    account = models.DecimalField(max_digits=12,decimal_places=2)
    cash = models.DecimalField(max_digits=12,decimal_places=2)
    stockValue = models.FloatField()