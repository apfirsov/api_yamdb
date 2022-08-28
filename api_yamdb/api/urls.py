from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, ReviewViewSet, TokenView, UserViewSet,
                    sign_up_view)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'),
v1_router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/signup/',
        sign_up_view,
        name='signup'),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='token_obtain'
    )
]
