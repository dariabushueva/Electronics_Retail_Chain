from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'last_name', 'first_name', 'email', 'phone', 'is_active')
    list_display_links = ('last_name', 'first_name', 'email', 'phone')
