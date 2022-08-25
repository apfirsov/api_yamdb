from api_yamdb.titles.models import Category, Genre, Title
from api_yamdb.titles.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, filters

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.AllowAny]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year') 
