from rest_framework.response import Response
from permissions import ReadOnly, IsAdmin, AuthorOrAdminOrModeratOrReadOnly
from serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleOnlyReadSerializer,
)
from reviews.models import Category, Genre, Title
from mixins import CreateUpdateDeleteViewSet
from rest_framework.pagination import PageNumberPagination


class CategoryViewSet(CreateUpdateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly, IsAdmin]
    pagination_class = PageNumberPagination


class GenreViewSet(CreateUpdateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly, IsAdmin]
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [ReadOnly, IsAdmin]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleOnlyReadSerializer
        return TitleSerializer
