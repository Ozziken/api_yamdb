import uuid


def make_confirmation_code():
    return uuid.uuid4()


def check_confirmation_code(user, confirmation_code) -> bool:
    return user.confirmation_code == confirmation_code
