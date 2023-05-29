from .models import Order
from rest_framework.response import Response
from rest_framework import status
from utils.services import get_longitude_longitude, get_data


def validate_order(pk, cur_status: str, courier_id: int = None):
    order = Order.objects.filter(id=pk).first()
    if not order:
        return Response(
            {'error': 'Order not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if order.status != cur_status:
        return Response(
            {'error': 'Order is not available'},
            status=status.HTTP_400_BAD_REQUEST
        )


def calc_price(order):
    ptA = get_longitude_longitude(order.con_id.address_id)
    ptB = get_longitude_longitude(order.address_id)
    data = get_data(ptA, ptB)
    last_order = Order.objects.filter(client_iin=order.client_iin).last()
    try:
        time_spent = data['rows'][0]['elements'][0]['duration']['text'].split(' ')[0]
        order.price = 400 + int(time_spent) * 65
        if last_order:
            order.price -= last_order.price * 0.1
            order.price = max(400, order.price)
        order.save()
    except Exception as e:
        print(e)
