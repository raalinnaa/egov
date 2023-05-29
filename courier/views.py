from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny

from courier.models import CourierCenter
from courier.serializers import CourierCenterSerializer, CourierCenterCreateSerializer


class CouriersCenterViewSet(viewsets.mixins.ListModelMixin,
                            viewsets.mixins.RetrieveModelMixin,
                            viewsets.mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return CourierCenterCreateSerializer
        return CourierCenterSerializer

    def get_queryset(self):
        return CourierCenter.objects.all()

