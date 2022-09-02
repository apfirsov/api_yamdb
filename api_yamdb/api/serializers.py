import datetime as dt
from django.contrib.auth import authenticate
from django.core.validators import MaxValueValidator
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class TokenSerializer(serializers.Serializer):
    "Token serializer."

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs['username'],
            'confirmation_code': attrs['confirmation_code'],
        }

        self.user = authenticate(**authenticate_kwargs)

        if not self.user:
            raise exceptions.ParseError('Аккаунт не найден')

        token = AccessToken.for_user(self.user)
        return {'token': str(token)}


class SignUpSerializer(serializers.ModelSerializer):
    """Signup user model serializer."""

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Используйте другое имя')
        return data


class UserSerializerForAdmin(serializers.ModelSerializer):
    """User model serializer for admin."""

    class Meta:
        abstract = True
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        unique = ('username', 'email')


class UserSerializerForUser(UserSerializerForAdmin):
    """User model serializer for user."""

    class Meta(UserSerializerForAdmin.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Genre model serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Title model serializer."""

    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(
        validators=[MaxValueValidator(dt.date.today().year)]
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category', 'rating',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Read only title model serializer."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category', 'rating',
        )
        read_only_fields = ('__all__',)


class ReviewSerializer(serializers.ModelSerializer):
    """Review model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')

    def create(self, validated_data):
        if validated_data['author'].reviews.filter(
                title=validated_data['title']).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв')

        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('review', 'id', 'author', 'text', 'pub_date')
        read_only_fields = ('review',)
