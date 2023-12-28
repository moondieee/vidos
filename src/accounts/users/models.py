from django.db import models

from django.contrib.auth.models import AbstractUser

from .managers import UserManager

USER_ROLE_CHOICES = (
    ('ADMIN', 'Админ'),
    ('CUSTOMER', 'Клиент')
)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=255,
        blank=True,
        null=True
    )
    company = models.CharField(
        verbose_name='Название компании',
        max_length=255,
        blank=True,
        null=True
    )
    crm = models.PositiveIntegerField(
        verbose_name='crm объект клиента',
        default=0
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE_CHOICES,
        default='CUSTOMER'
    )
    objects = UserManager()

    @property
    def is_customer(self):
        return self.role == 'CUSTOMER'

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
