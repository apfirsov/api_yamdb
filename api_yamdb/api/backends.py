from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from titles.models import Title
from users.models import User

from dataclasses import dataclass


class AuthBackend(ModelBackend):
    """Provides token authentication."""

    def authenticate(self, request, username=None, confirmation_code=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound('Пользователь не найден')
        if not default_token_generator.check_token(user, confirmation_code):
            raise exceptions.ParseError('Введен неправильный код потверждения')
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class TitleFilter(FilterSet):
    """"Django backend filter for title model."""

    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name='year',
    )

    class Meta:
        model = Title
        fields = '__all__'


@dataclass
class ConfirmationManager():

    user: User

    def get_message(self):
        """Forms a message with confirmationn code to be sent."""

        confirmation_code = default_token_generator.make_token(self.user)

        data = {}
        data['from_email'] = 'admin@yamdb.com'
        data['subject'] = 'Код подтверждения регистрации в api_yamdb'
        data['recipient_list'] = [self.user.email]
        data['message'] = f'''
        Имя пользователя: {self.user.username}
        confirmation_code: {confirmation_code}
        '''
        return data

    def send_code(self):
        """Sends an email verification code."""

        send_mail(
            **self.get_message(), fail_silently=False)

    def get_token(self):
        """Prints out JWT tokens to console."""

        refresh = RefreshToken.for_user(self.user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
