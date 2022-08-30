from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ReviewViewSet,
    GenreViewSet,
    TitleViewSet,
    CategoryViewSet,
)
from .views import (CommentViewSet, ReviewViewSet, TokenView, UserViewSet, SignupView)


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'),
v1_router.register('users', UserViewSet, basename='user')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/signup/',
        SignupView.as_view(),
        name='signup'),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='token_obtain'
    )
]
