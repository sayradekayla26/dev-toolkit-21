import functools
import time
import uuid
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def memoize(func: Callable):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def generate_id(prefix: str = "dev") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def pipeline(*funcs: Callable) -> Callable:
    def execute(value: Any):
        for func in funcs:
            value = func(value)
        return value
    return execute