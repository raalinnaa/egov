from django.contrib import admin
from utils.models import *


# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'oblast', 'city', 'street', 'house_number', 'apartment', 'entrance', 'floor', 'housing', 'residential_complex')
    search_fields = (
        'id', 'oblast', 'city', 'street', 'house_number', 'apartment', 'entrance', 'floor', 'housing', 'residential_complex')
    list_filter = (
        'id', 'oblast', 'city', 'street', 'house_number', 'apartment', 'entrance', 'floor', 'housing', 'residential_complex')
