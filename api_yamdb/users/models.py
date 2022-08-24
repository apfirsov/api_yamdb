from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRoles(models.TextChoices):
        USER = 'USR', 'Пользователь'
        MODERATOR = 'MOD', 'Модератор'
        ADMIN = 'ADM', 'Администратор'

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
        choices=UserRoles.choices,
        default=UserRoles.USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
