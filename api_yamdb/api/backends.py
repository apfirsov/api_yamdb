from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken
from titles.models import Title
from users.models import User


class AuthBackend(ModelBackend):
    """Provides token authentication."""

    def authenticate(self, request, username=None, confirmation_code=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound('Пользователь не найден')
        if not default_token_generator.check_token(user, confirmation_code):
            raise exceptions.ParseError('Аккаунт не найден')
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


class Utils():

    def send_confirmation_code(user):
        """Sends an email verification code."""

        confirmation_code = default_token_generator.make_token(user)

        from_email = 'admin@yamdb.com'
        subject = 'Код подтверждения регистрации в api_yamdb'
        message = f'''
        Имя пользователя: {user.username}
        confirmation_code: {confirmation_code}
        '''

        send_mail(
            subject, message, from_email, [user.email], fail_silently=False)

    def get_token(user):
        """Prints out JWT access token value to console."""

        token = AccessToken.for_user(user)
        return {'token': str(token)}
