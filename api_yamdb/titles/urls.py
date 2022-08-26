from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet,
    TitleViewSet,
    CategoryViewSet,
)

router = DefaultRouter()

router.register('genre', GenreViewSet)
router.register('title', TitleViewSet)
router.register('category', CategoryViewSet)

# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]

