from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from reviews.models import Category, Comment, Genre, Review, Title

from django.shortcuts import get_object_or_404

from api.mixins import CreateUpdateDeleteViewSet
from api.permissions import (
    AuthorOrAdminOrModeratOrReadOnly,
    IsAdminOrReadOnly,
    IsAuthor,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleOnlyReadSerializer,
    TitleSerializer,
)


class CategoryViewSet(CreateUpdateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class GenreViewSet(CreateUpdateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleOnlyReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет модели ревью на произведение."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    pagination_class = PageNumberPagination
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Review, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели комментария к ревью на произведение."""

    permission_classes = (
        IsAuthor,
        AuthorOrAdminOrModeratOrReadOnly,
    )
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
