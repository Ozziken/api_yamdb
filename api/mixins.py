from rest_framework import mixins, viewsets


class CreateUpdateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass
