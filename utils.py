import hashlib


def generate_short_url(url:str, length=8) -> str:

    hash = hashlib.md5(url.encode()).hexdigest()
    return hash[:length]


def generate_collision_safe_code(url:str):
    code = generate_short_url(url)