import time
import functools
import collections
from typing import Callable, Any, Dict

def memoize_with_ttl(seconds: int = 300):
    """creative cache with expiration using closure state"""
    cache = {}
    expiry = {}

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key not in cache or (now - expiry.get(key, 0) > seconds):
                cache[key] = func(*args, **kwargs)
                expiry[key] = now
            return cache[key]
        return wrapper
    return decorator

def deep_update(source: Dict, overrides: Dict) -> Dict:
    """recursive dictionary fusion for complex configuration objects"""
    for key, value in overrides.items():
        if isinstance(value, collections.abc.Mapping) and value:
            source[key] = deep_update(source.get(key, {}), value)
        else:
            source[key] = overrides[key]
    return source

def retry_operation(attempts: int = 3, delay: float = 1.0):
    """robust execution wrapper for volatile external interactions"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator