from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from con.serializers import ConSerializer
from con.models import Con
from orders.models import OTP
from orders.models import Order
from users.permissions import IsStaffUser
from utils.services import generate_otp, send_sms, get_phone
from orders.services import validate_order
from orders.serializers import OrderSerializer


class ConViewSet(viewsets.mixins.CreateModelMixin,
                 viewsets.mixins.ListModelMixin,
                 viewsets.mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [IsStaffUser, ]

    def get_serializer_class(self):
        return ConSerializer

    def get_queryset(self):
        return Con.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='order_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Order id',
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], permission_classes=[IsStaffUser, ])
    def send_otp(self, request):
        courier_id = request.user.id
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response(
                {'error': 'Order id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = validate_order(order_id, 'in_progress', courier_id)
        if response:
            return response
        order = Order.objects.filter(id=order_id).first()
        otp_code = generate_otp()
        OTP.objects.create(
            order_id=order,
            otp=otp_code
        )
        response = send_sms(order.courier_id.phone, otp_code)
        if response.get('status') != 'OK':
            return Response(
                {'error': 'SMS not sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'OTP sent'})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='otp_code',
                type=OpenApiTypes.STR,
                required=True
            ),
            OpenApiParameter(
                name='order_id',
                type=OpenApiTypes.INT,
                required=True
            ),

        ]
    )
    @action(detail=False, methods=['get'], permission_classes=[IsStaffUser, ])
    def verify_otp(self, request):
        otp_code = request.query_params.get('otp_code')
        order_id = request.query_params.get('order_id')
        order = Order.objects.filter(id=order_id).first()
        response = validate_order(order_id, 'in_progress', request.user.id)
        if response:
            return response
        if not otp_code:
            return Response(
                {'error': 'OTP code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        otp = OTP.objects.filter(
            order_id=order_id,
            otp=otp_code,
            created_at__gte=timezone.now() - timedelta(minutes=1),
            is_verified_by_con=False
        ).first()
        if not otp:
            return Response(
                {'error': 'OTP not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if otp.is_verified_by_con:
            return Response(
                {'error': 'OTP already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        otp.is_verified_by_con = True
        otp.save()
        phone = get_phone(order.taker_iin)
        if not phone:
            return Response(
                {'error': 'Phone not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = send_sms(phone, f'Your order is on the way, {order.courier_id.first_name} {order.courier_id.phone}')
        if response.status_code != 200:
            return Response(
                {'error': 'SMS not sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'OTP verified'})

    @action(detail=True, methods=['get'], permission_classes=[IsStaffUser, ])
    def orders(self, request, pk):
        orders = Order.objects.filter(
            con_id=pk,
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

