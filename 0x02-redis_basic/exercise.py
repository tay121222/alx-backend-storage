#!/usr/bin/env python3
"""A Cache class"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """ store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
            fn: Optional[Callable[[bytes], Union[str, bytes, int]]] = None
            ) -> Union[str, bytes, int, None]:
        """get method that take a key string argument and an
        optional Callable argument named fn"""
        data = self._redis.get(key)
        return fn(data) if data is not None and fn else data

    def get_str(self, key: str) -> Optional[str]:
        """will automatically parametrize Cache.get"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """will automatically parametrize Cache.get"""
        return self.get(key, fn=int)
