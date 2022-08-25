from rest_framework import serializers
from api_yamdb.titles.models import (
    Category, Genre, GenreTitle, Title
)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Category
#         fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


# class GenreTitleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = GenreTitle
#         fields = '__all__'


