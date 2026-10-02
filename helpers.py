import time
import re
from functools import wraps
from typing import Any, Callable, Dict, Iterable


def safe_get(data: Any, path: str, default: Any = None) -> Any:
    """Navigate nested dicts, lists, or objects using string path expression."""
    tokens = re.findall(r'[^\.\[\]]+|\d+', path)
    current = data
    for token in tokens:
        if current is None:
            return default
        if isinstance(current, dict):
            current = current.get(token, default)
        elif isinstance(current, (list, tuple)):
            idx = int(token) if token.isdigit() else -1
            if 0 <= idx < len(current):
                current = current[idx]
            else:
                return default
        elif hasattr(current, token):
            current = getattr(current, token)
        else:
            return default
    return current


def timed_cache(ttl_seconds: float = 60.0):
    """Decorator caching function returns with monotonic expiration clock."""
    def decorator(func: Callable):
        cache: Dict[tuple, tuple] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in cache:
                timestamp, result = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result

        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator


def pipe(initial_value: Any, *funcs: Callable) -> Any:
    """Thread a value sequentially through a chain of callable operations."""
    result = initial_value
    for fn in funcs:
        result = fn(result)
    return result


def chunk_iterable(iterable: Iterable, chunk_size: int):
    """Lazy chunk generator for arbitrary iterable sequences."""
    iterator = iter(iterable)
    while True:
        chunk = []
        for _ in range(chunk_size):
            try:
                chunk.append(next(iterator))
            except StopIteration:
                break
        if not chunk:
            break
        yield chunk
