from rest_framework import serializers
from .models import CourierCenter, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'oblast',
            'city',
            'street',
            'house_number',
            'apartment',
            'entrance',
            'floor',
            'housing',
            'residential_complex',
            'additional_info',
        ]


class CourierCenterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = CourierCenter
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'email',
            'is_active',
            'created_at',
            'updated_at'
        ]


class CourierCenterCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourierCenter
        fields = [
            'name',
            'address_id',
            'phone',
            'email',
        ]
