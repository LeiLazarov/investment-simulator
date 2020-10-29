from django.db import models

class Statistic(models.Model):
    userID = models.IntegerField(primary_key=True)
    account = models.float(max_length=64)
    cash = models.IntegerField()
    avg_price = models.FloatField()
    min_price = models.FloatField()
    max_price = models.FloatField()