from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrAdminOrModeratOrReadOnly(BasePermission):
    """Для комментариев."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    Проверка на авторизацию для всех методов, кроме POST
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_staff
