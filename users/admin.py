from django.contrib import admin
from users.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
    search_fields = (
        'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
    list_filter = (
        'id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
