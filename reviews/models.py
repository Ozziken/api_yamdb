from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = (
    get_user_model()
)  # Нужно добавить кастомную модель https://code.s3.yandex.net/backend-developer/learning-materials/custom_User_model.pdf


class Category(models.Model):
    slug = models.SlugField(
        "Slug",
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        "Название",
        max_length=256,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    slug = models.SlugField(
        "Slug",
        max_length=50,
        unique=True,
    )
    name = models.CharField(
        "Название",
        max_length=256,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="titles",
    )
    description = models.TextField(
        "Описание",
        db_index=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр",
        related_name="titles",
    )
    name = models.CharField(
        "Название",
        max_length=256,
        db_index=True,
        related_name="titles",
    )
    year = models.IntegerField(
        "Год выпуска",
        null=False,
        db_index=True,
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        "Оценка",
        null=False,
        db_index=True,
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_message={"validators": "Оценка может быть только от 1 до 10"},
    )
    text = models.TextField("Текс оценки", null=False, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор оценки"
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"


class Comment(models.Model):
    text = models.TextField("Текс комментария", null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор комментария"
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name="Оценка")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
