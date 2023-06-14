from string import digits

from django.utils.crypto import get_random_string


def send(**kwargs) -> dict:
    return {'success': True, 'code': get_random_string(length=6, allowed_chars=digits)}
