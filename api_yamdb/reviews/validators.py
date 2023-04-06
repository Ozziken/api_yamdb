from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """
    Валидатор для поля год в модели Title.
    Проверяет, что год находится в диапазоне от 1900 до текущего года.
    """
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        raise ValidationError(
            "Год должен быть от 1900 до {}.".format(current_year)
        )
