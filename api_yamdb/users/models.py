import uuid

from users.validators import CustomUsernameValidator

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_me

CHOICES = (
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
)


class User(AbstractUser):
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        validators=[CustomUsernameValidator(), username_me],
        error_messages={
            "unique": (
                "Пользователь с таким именем пользователя уже существует."
            ),
        },
    )
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=254,
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
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=16,
        choices=CHOICES,
        default="user",
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
        return self.is_staff or self.role == settings.ADMIN

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    class Meta:
        ordering = ("-id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
