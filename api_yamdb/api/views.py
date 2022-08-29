from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail

from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from reviews.models import Comment, Review
from users.models import User
from .permissions import ReviewsCommentsPermission, IsAdmin
from titles.models import Category, Genre, Title
from django.db.models import Avg
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    """Post model view set."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewsCommentsPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment model view set."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewsCommentsPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        return review.comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(viewsets.ModelViewSet):
    """Genre model view set."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    """Category model view set."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Title model view set."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

@api_view(['POST', ])
def sign_up_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        serializer.save()
        send_confirmation_code(user=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения регистрации в api_yamdb',
        f'''Имя пользователя: {user.username}
confirmation_code: {confirmation_code}''',
        'admin@yamdb.com',
        [user.email],
        fail_silently=False
    )


class TokenView(TokenViewBase):
    serializer_class = TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )

    @action(detail=False, methods=['GET', 'PATCH'], name='My information')
    def me(self, request, *args, **kwargs):
        my_user_instance = User.objects.get(username=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(my_user_instance)
            return Response(serializer.data)
        serializer = self.get_serializer(
            my_user_instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
