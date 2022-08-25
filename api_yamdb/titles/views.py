from api_yamdb.titles.models import Categorie, Genre, Title
from api_yamdb.titles.serializers import (
    CategorieSerializer, GenreSerializer, TitleSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

# class GenreViewSet(viewsets.ModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = [permissions.AllowAny]


# class CategorieViewSet(viewsets.ModelViewSet):
#     queryset = Categorie.objects.all()
#     serializer_class = CategorieSerializer
#     permission_classes = [permissions.AllowAny]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year') 
