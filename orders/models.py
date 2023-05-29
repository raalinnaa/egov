from django.db import models
from django.utils.translation import gettext as _

from mixins.models import TimeStampMixin, IsActiveMixin
from con.models import Con
from utils.models import Address
from users.models import User
from courier.models import CourierCenter


class Order(TimeStampMixin, IsActiveMixin):
    request_id = models.CharField(
        max_length=255,
        verbose_name=_('Order number'),
    )
    courier_center_id = models.ForeignKey(
        CourierCenter,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Courier center'),
    )
    courier_id = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('Courier'),
    )
    address_id = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        verbose_name=_('Address'),
    )
    con_id = models.ForeignKey(
        Con,
        on_delete=models.CASCADE,
        verbose_name=_('Con'),
    )
    client_iin = models.CharField(
        max_length=255,
        verbose_name=_('Client IIN'),
    )
    taker_iin = models.CharField(
        max_length=255,
        verbose_name=_('Taker IIN'),
    )
    STATUS = [
        ('pending', _('Pending')),
        ('in_progress', _('In progress')),
        ('done', _('Done')),
    ]
    status = models.CharField(
        choices=STATUS,
        max_length=255,
        verbose_name=_('Status'),
    )
    price = models.FloatField(
        verbose_name=_('Price'),
        null=True,
        blank=True,
        default=0,
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"{self.id} - {self.request_id} - {self.status}"


class OrderHistory(TimeStampMixin, IsActiveMixin):
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
    )

    old_status = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Old status'),
    )
    new_status = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('New status'),
    )
    old_courier_id = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='old_courier',
        verbose_name=_('Old courier'),
    )
    new_courier_id = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='new_courier',
        verbose_name=_('New courier'),
    )

    class Meta:
        verbose_name = _('OrderHistory')
        verbose_name_plural = _('OrderHistories')

    def __str__(self):
        return f"{self.id}"


class OTP(TimeStampMixin, IsActiveMixin):
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
    )
    otp = models.CharField(
        max_length=255,
        verbose_name=_('OTP'),
    )
    is_verified_by_con = models.BooleanField(
        default=False,
        verbose_name=_('Is verified by con'),
    )

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')

    def __str__(self):
        return f"{self.id}"
