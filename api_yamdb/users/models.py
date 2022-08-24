from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=3,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES.USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
