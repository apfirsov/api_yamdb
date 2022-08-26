from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ReviewViewSet,
    GenreViewSet,
    TitleViewSet,
    CategoryViewSet,
)


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'),

# Урлы для теста кода, потом подвести под общий формат
v1_router.register('genre', GenreViewSet)
v1_router.register('title', TitleViewSet)
v1_router.register('category', CategoryViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
