from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^(?!me\b)[\w.@+-]+$'
    message = (
        'Имя пользователя может содержать только буквы, цифры и символы '
        '@/./+/-/_. Использовать имя "me" в качестве username запрещено'
    )
    flags = 0
