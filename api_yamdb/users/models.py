from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = [
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
]


class User(AbstractUser):
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
