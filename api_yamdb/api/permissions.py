from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import User


class IsAdmin(BasePermission):
    '''...'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_superuser or request.user.role == User.ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.role == User.ADMIN)


class IsAdminOrReadOnly(BasePermission):
    ''' Categories, Genres, Titles '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                or (request.user
                    and request.user.is_authenticated
                    and request.user.role == User.ADMIN)
                )


class IsAuthorOrAdmin(BasePermission):
    ''' users/me '''

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_superuser
                or request.user.role == User.ADMIN)


class ReviewsCommentsPermission(BasePermission):
    ''' Reviews, Comments.
        Юзеру доступен метод POST
        Автору, админу и модератору доступны методы PATCH, DELETE
        SAFE методы доступны всем '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role in [User.ADMIN, User.MODERATOR])
                )
