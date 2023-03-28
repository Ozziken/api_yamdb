from rest_framework import permissions


class AuthorOrAdminOrModeratOrReadOnly(permissions.BasePermission):
    """Для комментариев."""

    def has_object_permission(self, request):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_author
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user


class IsAdmin(permissions.BasePermission):
    """Добавление/обновление информации о
    произведении или удаление произведения.
    Добавление или удаление категорий.
    Добавление или удаление жанров.

    """

    def has_object_permission(self, request):
        return request.user.is_admin == request.user


class ReadOnly(permissions.BasePermission):
    """Информаия о произведении. Получение всех отзывов."""

    def has_object_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
