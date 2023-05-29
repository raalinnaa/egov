from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext as _

from mixins.models import (
    TimeStampMixin,
    IsActiveMixin,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStampMixin,
    IsActiveMixin,
):
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('First name'),
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Last name'),
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('Email'),
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name=_('Phone'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Staff status'),
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_('Superuser status'),
        help_text=_('Superuser can do anything.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active status'),
        help_text=_('Active status of user.'),
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
