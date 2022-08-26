from rest_framework import serializers
from reviews.models import Comment, Review
from titles.models import (
    Category, Genre, Title
)


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






class GenreSerializer(serializers.ModelSerializer):
    """Genre model serializer."""

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """CommTitleent model serializer."""

    class Meta:
        model = Title
        fields = '__all__'


# class GenreTitleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = GenreTitle
#         fields = '__all__'
