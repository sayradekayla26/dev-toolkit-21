import functools
import time
import collections
from typing import Callable, Any, Dict

def memoize(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def retry(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def flatten(iterable: Any) -> list:
    items = []
    for item in iterable:
        if isinstance(item, (list, tuple)):
            items.extend(flatten(item))
        else:
            items.append(item)
    return items

def chunker(seq: list, size: int):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

class Registry(dict):
    def register(self, key: str):
        def wrapper(func: Callable):
            self[key] = func
            return func
        return wrapper