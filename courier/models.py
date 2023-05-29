from django.db import models

from django.utils.translation import gettext as _

from mixins.models import TimeStampMixin, IsActiveMixin
from utils.models import Address
from users.models import User


class CourierCenter(TimeStampMixin, IsActiveMixin):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    address_id = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Address'),
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Phone'),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Email'),
    )

    class Meta:
        verbose_name = _('CourierCenter')
        verbose_name_plural = _('CourierCenters')

    def __str__(self):
        return self.name


class CourierCourierCenter(TimeStampMixin, IsActiveMixin):
    courier_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Courier'),
    )
    courier_center_id = models.ForeignKey(
        CourierCenter,
        on_delete=models.CASCADE,
        verbose_name=_('CourierCenter'),
    )

    class Meta:
        verbose_name = _('CourierCourierCenter')
        verbose_name_plural = _('CourierCourierCenters')

    def __str__(self):
        return self.id

