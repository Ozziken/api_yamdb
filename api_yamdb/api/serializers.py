import datetime as dt

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    year = serializers.IntegerField()
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

        def validate_year(self, data):
            if data >= dt.datetime.now().year:
                raise serializers.ValidationError(
                    "Год произведения не может быть больше текущего!",
                )
            return data


class TitleOnlyReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментария к ревью."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = (
            "id",
            "author",
            "text",
            "created",
        )
        model = Comment
        read_only_fields = ("review",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели ревью на произведение."""

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title",
    )
    score = serializers.IntegerField()
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    read_only_fields = (
        "id",
        "pub_date",
        "author",
    )

    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        fields = (
            "id",
            "text",
            "pub_date",
            "author",
            "title",
            "rating",
            "comments",
        )
        model = Review
