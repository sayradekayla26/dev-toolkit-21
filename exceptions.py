import functools
import time
import logging

logger = logging.getLogger('dev-toolkit-21')

class PerformanceOptimizer:
    """Reactive memoization cache for compute-intensive tasks."""
    def __init__(self, ttl=60):
        self._cache = {}
        self._ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in self._cache:
                result, timestamp = self._cache[key]
                if now - timestamp < self._ttl:
                    return result
            result = func(*args, **kwargs)
            self._cache[key] = (result, now)
            return result
        return wrapper

class CacheOverflowError(Exception):
    """Custom exception for cache memory exhaustion."""
    pass

def memory_safe_decorator(limit=1000):
    """Decorator preventing cache bloat in core."""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(cache) >= limit:
                raise CacheOverflowError("Cache memory limit reached")
            res = func(*args, **kwargs)
            cache[str(args)] = res
            return res
        return wrapper
    return decorator