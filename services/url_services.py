# swoop
# x60,email js,
from typing import Any

from werkzeug.exceptions import BadRequest, NotFound

from database import db
from models.url import Url
from redis_client import get_redis
from utils import is_valid_url, generate_short_url

redis = get_redis()

def get_short_code(original_url:str)-> dict[str, str | Any] | None:
    if not is_valid_url(original_url):
        raise BadRequest("Invalid Url")

    short_code = generate_short_url(original_url)
    cached_url = redis.get(f"url:{short_code}")

    if cached_url is not None:
        if cached_url == original_url:
            return {
                "short_code": short_code,
                "short_url": f"http://localhost:5000/{short_code}",
                "original_url": original_url
            }
        else:
            short_code = generate_short_url(original_url, 10)

    existing = Url.query.filter_by(generated_url=short_code).first()
    if existing is not None:
        if existing.original_url == original_url:
            redis.setex(f"url:{short_code}", 3600, original_url)
            return {
                "short_code": short_code,
                "short_url": f"http://localhost:5000/{short_code}",
                "original_url": original_url
            }
        else:
            short_code = generate_short_url(original_url, 10)

    new_url = Url(original_url=original_url, generated_url=short_code)
    db.session.add(new_url)
    db.session.commit()

    redis.setex(f"url:{short_code}", 3600, original_url)

    return{
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}",
        "original_url": original_url
    }

def get_original_url(short_code:str):
    original_url = redis.get(f"url:{short_code}")

    if not original_url:
        url = Url.query.filter_by(generated_url=short_code).first()

        if not url:
            raise BadRequest("Invalid Short Url")

        original_url = url.original_url
        redis.setex(f"url:{short_code}", 3600, original_url)
    redis.incr(f"clicks:{short_code}")

    return original_url


def get_stats(short_code:str):
    url_entry = Url.query.filter_by(generated_url=short_code).first()

    if not url_entry:
        raise NotFound("Short URL not found")

    clicks = redis.get(f"clicks:{short_code}")

    return {
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}",
        "original_url": url_entry.original_url,
        "clicks": int(clicks) if clicks else 0,
        "created_at": url_entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }