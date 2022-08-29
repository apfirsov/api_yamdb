from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from users.models import User


class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None, confirmation_code=None):
        user = User.objects.get(username=username)
        print(confirmation_code)
        if default_token_generator.check_token(user, confirmation_code):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
