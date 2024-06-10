"""
User class used as an authentication user object.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE_CHOICES = (
    ('ADMIN', 'Админ'),
    ('CUSTOMER', 'Клиент')
)


class User(AbstractUser):
    """
    Object for describing a User from the authorization service 'accounts'.
    """
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

    # Don't use User in the database, so exclude this relationship
    groups = None
    user_permissions = None
