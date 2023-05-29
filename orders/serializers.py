from rest_framework import serializers

from con.serializers import ConSerializer
from courier.serializers import AddressSerializer
from users.serializers import UserListSerializer
from .models import Order
from utils.models import Address


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
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'request_id',
            'courier_id',
            'address_id',
            'con_id',
            'client_iin',
            'taker_iin',
            'status',
        ]


class OrderFullSerializer(serializers.ModelSerializer):
    address_id = AddressSerializer()
    courier_id = UserListSerializer()
    con_id = ConSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'request_id',
            'courier_id',
            'address_id',
            'con_id',
            'client_iin',
            'taker_iin',
            'price',
            'status',
        ]


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(
        max_length=6,
        min_length=6,
    )
