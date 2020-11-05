from django.db import models


# Create your models here.
from login.models import User


class WatchList(models.Model):
    symbol = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name='watchlist', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'WatchList_' + self.symbol

    class Meta:
        verbose_name_plural = 'WatchLists'
        ordering = ['-createdAt']

