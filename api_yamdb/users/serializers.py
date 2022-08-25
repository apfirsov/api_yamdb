from rest_framework import serializers, exceptions
from .models import User
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class MyTokenObtainSerializer(TokenObtainSerializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        code_is_valid = default_token_generator.check_token(
            self.username_field,
            attrs['confirmation_code']
        )
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field]
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if (not api_settings.USER_AUTHENTICATION_RULE(self.user)
                and not code_is_valid):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}


class MyTokenObtainSlidingSerializer(MyTokenObtainSerializer):
    token_class = SlidingToken

    def validate(self, attrs):
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


# class MyBackend:
#     def authenticate(self,
#                      request,
#                      username=None,
#                      confirmation_code=None):
#         pass
