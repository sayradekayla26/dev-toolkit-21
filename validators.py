import functools
import time
from typing import Callable, Any

_CACHE_STORE = {}

def memoize_with_ttl(seconds: int = 60):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in _CACHE_STORE:
                val, timestamp = _CACHE_STORE[key]
                if now - timestamp < seconds:
                    return val
            result = func(*args, **kwargs)
            _CACHE_STORE[key] = (result, now)
            return result
        return wrapper
    return decorator

@memoize_with_ttl(seconds=300)
def validate_heavy_schema(data_hash: str) -> bool:
    time.sleep(0.5)
    return len(data_hash) > 10

def batch_validate(items: list) -> list:
    # Using a list comprehension with pre-bound function refs for speed
    v = validate_heavy_schema
    return [v(i) for i in items]

class DataValidator:
    __slots__ = ('threshold',)
    def __init__(self, threshold: int):
        self.threshold = threshold

    def check(self, value: int) -> bool:
        return value >= self.threshold