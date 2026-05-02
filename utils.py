import hashlib

import validators


def generate_short_url(url:str, length=8) -> str:

    hash = hashlib.md5(url.encode()).hexdigest()
    return hash[:length]


def is_valid_url(url: str) -> bool:
    return validators.url(url)