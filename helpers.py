import functools
import time
import logging
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def deep_freeze(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(deep_freeze(i) for i in obj)
    elif isinstance(obj, dict):
        return frozenset((k, deep_freeze(v)) for k, v in obj.items())
    return obj

def time_execution(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logging.info(f"execution of {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]