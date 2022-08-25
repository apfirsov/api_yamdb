from rest_framework import serializers
from reviews.models import Comment, Review


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
