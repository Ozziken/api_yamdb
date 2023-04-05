from rest_framework import mixins, viewsets

from .permissions import IsAdminOrReadOnly


class CreateUpdateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Кастомный миксин для жанров и категорий."""

    permission_classes = (IsAdminOrReadOnly,)
