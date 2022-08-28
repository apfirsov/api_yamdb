from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ReviewViewSet,
    UserViewSet,
    sign_up_view,
    TokenView
)


v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'),
v1_router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'signup/',
        sign_up_view,
        name='signup'),
    path(
        'token/',
        TokenView.as_view(),
        name='token_obtain_pair'
    ),
    path('', include(v1_router.urls))
]
