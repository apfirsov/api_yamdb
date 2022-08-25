from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ReviewViewSet,
)


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'),

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
