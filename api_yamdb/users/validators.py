from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r"^(?!me\b)[\w.@+-]+$"
    message = (
        "Имя пользователя может содержать только буквы, цифры и символы "
        '@/./+/-/_. Использовать имя "me" в качестве username запрещено'
    )
    flags = 0


def username_me(value):
    """Проверка имени пользователя (me недопустимое имя)."""
    if value == "me":
        raise ValidationError('Имя пользователя "me" не разрешено.')
    return value
