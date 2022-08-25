from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import sign_up_view, MyTokenObtainSlidingView, UserViewSet


router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path(
        'signup/',
        sign_up_view,
        name='signup'),
    path(
        'token/',
        MyTokenObtainSlidingView.as_view(),
        name='token_obtain_pair'
    ),
    path('', include(router.urls))
]
