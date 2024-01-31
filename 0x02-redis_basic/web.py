#!/usr/bin/env python3
"""get_page function that requests module to obtain
the HTML content of a particular URL"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def decorator(func: Callable) -> Callable:
    """Decorator wrapper"""

    @wraps(func)
    def wrapper(url):
        """ just a wrapper"""

        redis_client.incr("count:{}".format(url))
        cached_response = redis_client.get("cached:{}".format(url))
        if cached_response:
            return cached_response.decode('utf-8')
        response = func(url)
        redis_client.setex("cached:{}".format(url), 10, response)

        return response

    return wrapper


@decorator
def get_page(url: str) -> str:
    """Get the HTML content of given URL"""
    results = requests.get(url)
    return results.text
