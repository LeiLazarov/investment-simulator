from django.contrib import admin

# Register your models here.
from login.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'createdAt')


admin.site.register(User, UserAdmin)