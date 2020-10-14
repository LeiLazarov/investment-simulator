from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(blank=False, null=False, max_length=256)

    def __str__(self):
        return self.username

