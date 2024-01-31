#!/usr/bin/env python3
"""get_page function that requests module to obtain
the HTML content of a particular URL"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def track_access_and_cache(expiration: int = 10) -> Callable:
    """track the number of times a URL is accessed and cache the response."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client.incr("count:{}".format(url))
            cached_response = redis_client.get("cached:{}".format(url))
            if cached_response:
                return cached_response.decode('utf-8')
            response = func(url)
            redis_client.setex("cached:{}".format(url), expiration, response)

            return response

        return wrapper

    return decorator


@track_access_and_cache()
def get_page(url: str) -> str:
    """Get the HTML content of given URL"""
    return requests.get(url).text
