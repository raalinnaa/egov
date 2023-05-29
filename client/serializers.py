from rest_framework import serializers


class IINSerializer(serializers.Serializer):
    iin = serializers.CharField(
        max_length=12,
        min_length=12,
    )

