from django.contrib import admin
from .models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'password',)

admin.site.register(User, UsersAdmin)
