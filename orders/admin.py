from django.contrib import admin
from orders.models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'con_id', 'status', 'taker_iin', 'client_iin', 'created_at', 'updated_at')
    search_fields = ('id', 'con_id', 'status', 'taker_iin', 'client_iin',  'created_at', 'updated_at')
    list_filter = ('id', 'con_id', 'status', 'taker_iin', 'client_iin', 'created_at', 'updated_at')
