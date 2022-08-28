from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    ''' Users кроме методов GET и PATCH для префикса /me '''

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or (request.user
                    and request.user.is_authenticated
                    and request.user.role == 'admin')
                )


class IsAdminOrReadOnly(BasePermission):
    ''' Categories, Genres, Titles '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_superuser
                or (request.user
                    and request.user.is_authenticated
                    and request.user.role == 'admin')
                )


class IsAuthorOrAdmin(BasePermission):
    ''' users/me '''

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_superuser
                or request.user.role == 'admin')


class ReviewsCommentsPermission(BasePermission):
    ''' Reviews, Comments.
        Юзеру доступен метод POST
        Автору, админу и модератору доступны методы PATCH, DELETE
        SAFE методы доступны всем '''

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return (obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role in ['admin', 'moderator']
                    )
        return True
