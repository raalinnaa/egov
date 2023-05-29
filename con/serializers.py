from rest_framework import serializers

from .models import Con


class ConSerializer(serializers.ModelSerializer):
    class Meta:
        model = Con
        fields = [
            'id',
            'address_id',
            'email',
            'phone',
        ]
