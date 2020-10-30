from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(blank=False, null=False, max_length=256)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User' + self.username

    class Meta:
        verbose_name_plural = 'Users'


