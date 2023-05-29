from django.contrib import admin
from con.models import *


@admin.register(Con)
class ConAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address_id', 'email', 'phone')
    search_fields = ('name', 'address_id', 'email', 'phone')
    list_filter = ('name', 'address_id', 'email', 'phone')

