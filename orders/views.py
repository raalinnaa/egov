from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny

from courier.permission import IsCourier
from orders.serializers import OrderSerializer, AddressSerializer, OTPSerializer, OrderFullSerializer
from orders.models import Order, OTP
from users.models import User
from utils.services import send_sms, generate_otp, get_phone, get_longitude_longitude, get_data
from django.utils import timezone
from datetime import timedelta
from .services import validate_order, calc_price


class AddressViewSet(viewsets.mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        return AddressSerializer


class OrderViewSet(viewsets.mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderSerializer
        return OrderFullSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        calc_price(instance)
        return Response(OrderFullSerializer(instance).data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='courier_center_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Courier center id',
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def get_available_orders(self, request):
        courier_center_id = request.query_params.get('courier_center_id')
        if not courier_center_id:
            return Response(
                {'error': 'courier_center_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        orders = Order.objects.filter(
            courier_center_id=courier_center_id,
            status='pending'
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsCourier, ])
    def assign_to_courier(self, request, pk=None):
        courier_id = request.user
        response = validate_order(pk, 'pending')
        if response:
            return response
        order = Order.objects.filter(id=pk).first()
        order.courier_id = courier_id
        order.status = 'in_progress'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsCourier, ])
    def unassign_from_courier(self, request, pk=None):
        courier_id = request.user.id
        order = validate_order(pk, 'in_progress', courier_id)
        order.courier_id = None
        order.status = 'pending'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsCourier, ])
    def send_otp(self, request, pk=None):
        courier_id = request.user.id
        order = validate_order(pk, 'in_progress', courier_id)
        otp_code = generate_otp()
        OTP.objects.create(
            order_id=order.id,
            otp=otp_code,
            is_verified_by_con=True,
        )
        phone = get_phone(order.taker_iin)
        response = send_sms(phone, otp_code)
        if response.status_code != 200:
            return Response(
                {'error': 'SMS not sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'OTP sent'})

    @extend_schema(request=OTPSerializer)
    @action(detail=True, methods=['post'], permission_classes=[IsCourier, ])
    def verify_otp(self, request, pk=None):
        courier_id = request.user.id
        order = validate_order(pk, 'in_progress', courier_id)
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = OTP.objects.filter(
            order_id=order.id,
            otp=serializer.validated_data['otp'],
            is_verified_by_con=True,
        ).last()
        if otp.created_at < timezone.now() - timedelta(minutes=1):
            return Response(
                {'error': 'OTP is expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not otp:
            return Response(
                {'error': 'OTP is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'completed'
        order.save()
        return Response({'message': 'Order completed'})
