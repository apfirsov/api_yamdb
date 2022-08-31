from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.ADMIN))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.role == User.ADMIN)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.ADMIN))

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (request.user.is_superuser
                or request.user.role == User.ADMIN)


class IsUserOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj == request.user
                or request.user.is_superuser
                or request.user.role == User.ADMIN)


class AuthorOrStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role in [User.ADMIN, User.MODERATOR]))
