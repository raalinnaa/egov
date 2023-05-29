from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from utils.services import get_random_request_id, get_phone, send_sms, get_request_message, get_user_info

from client.serializers import IINSerializer


class RequestViewSet(viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    iin_param = OpenApiParameter(
        name='iin',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='iin',
        required=True
    )

    def get_serializer_class(self):
        return IINSerializer

    @extend_schema(
        parameters=[iin_param]
    )
    def list(self, request, *args, **kwargs):
        if request.query_params.get('iin', None) is None:
            return Response(
                {
                    'error': 'iin is required',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        random_request_id = get_random_request_id()
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        phone = get_phone(serializer.validated_data['iin']).get('phone', None)
        if phone is None:
            return Response(
                {
                    'error': 'Phone number not found',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        message = get_request_message(random_request_id)
        response = send_sms(phone, message)
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[iin_param]
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny, ])
    def get_user_info_by_iin(self, request):
        if not request.query_params.get('iin'):
            return Response(
                {'error': 'iin is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        response = get_user_info(iin=serializer.validated_data['iin'])
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[iin_param]
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny, ])
    def get_phone_by_iin(self, request):
        if not request.query_params.get('iin'):
            return Response(
                {'error': 'iin is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        response = get_phone(iin=serializer.validated_data['iin'])
        return Response(
            response,
            status=status.HTTP_200_OK
        )
