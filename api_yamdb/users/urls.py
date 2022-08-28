from django.urls import path, include
from rest_framework import routers
from .views import sign_up_view, UserViewSet, TokenView

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path(
        'signup/',
        sign_up_view,
        name='signup'),
    path(
        'token/',
        TokenView.as_view(),
        name='token_obtain_pair'
    ),
]
