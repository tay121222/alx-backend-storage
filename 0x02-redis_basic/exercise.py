#!/usr/bin/env python3
"""A Cache class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """decorator to store the history of inputs
    and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


def replay(func: Callable = None):
    """replay function to display the history of calls of
    a particular function"""
    method_name = func.__qualname__
    input_key = "{}:inputs".format(method_name)
    output_key = "{}:outputs".format(method_name)
    cache = redis.Redis()
    input_history = cache.lrange(input_key, 0, -1)
    output_history = cache.lrange(output_key, 0, -1)

    num_calls = len(input_history)

    print("{} was called {} times:".format(method_name, num_calls))

    for inputs, output in zip(input_history, output_history):
        print("{}(*{}) -> {}".format(
            method_name, inputs.decode('utf-8'), output.decode('utf-8')
            ))


class Cache:
    def __init__(self):
        """ store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        if type(data) in (int, float):
            data = str(data)
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, None]:
        """get method that take a key string argument and an
        optional Callable argument named fn"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Optional[str]:
        """will automatically parametrize Cache.get"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """will automatically parametrize Cache.get"""
        return self.get(key, lambda x: int(x))


Cache.store = count_calls(Cache.store)
