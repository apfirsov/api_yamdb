from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Comment, Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Review model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('review', 'id', 'author', 'text', 'pub_date')
        read_only_fields = ('review',)


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Используйте другое имя')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class TokenSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        attrs.update({'password': ''})
        try:
            username = list(attrs.items())[0][1]
            confirmation_code = list(attrs.items())[1][1]
        except AttributeError:
            raise exceptions.AuthenticationFailed('invalid data')
        user = User.objects.get(username=username)
        if default_token_generator.check_token(user, confirmation_code):
            return super(TokenSerializer, self).validate(attrs)
        raise exceptions.AuthenticationFailed('invalid confirmation code')


class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None):
        if username is None:
            username = request.data.get('username', '')
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
