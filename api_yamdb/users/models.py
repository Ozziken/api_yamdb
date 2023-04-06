import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import CustomUsernameValidator

from .validators import username_me


class Role(models.TextChoices):
    USER = "user", "Пользователь"
    MODERATOR = "moderator", "Модератор"
    ADMIN = "admin", "Администратор"


class User(AbstractUser):
    """Кастомная модельпользователя."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        validators=[CustomUsernameValidator(), username_me],
        error_messages={
            "unique": ("Пользователь с таким именем пользователя уже существует."),
        },
    )
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=254,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=16,
        choices=Role.choices,
        default=USER,
        error_messages={"validators": "Выбрана несуществующая роль"},
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    confirmation_code = models.UUIDField(
        "Код для получения/обновления токена",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ("-id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name
