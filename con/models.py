from django.db import models
from utils.models import Address
from django.utils.translation import gettext as _
from mixins.models import TimeStampMixin, IsActiveMixin
from users.models import User


class Con(TimeStampMixin, IsActiveMixin):
    name = models.CharField(
        max_length=255
    )
    address_id = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    email = models.EmailField(
        null=True,
        blank=True,
        max_length=255
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )

    class Meta:
        verbose_name = _('Con')
        verbose_name_plural = _('Cons')

    def __str__(self):
        return self.name


class StaffCon(TimeStampMixin, IsActiveMixin):
    staff_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    con_id = models.ForeignKey(
        Con,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('StaffCon')
        verbose_name_plural = _('StaffCons')

    def __str__(self):
        return f"{self.id}"
