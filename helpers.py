import json
import time
from typing import Any, Callable, TypeVar, ParamSpec
from functools import wraps

T = TypeVar('T')
P = ParamSpec('P')

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
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

def memoize_to_disk(filepath: str):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = str((args, kwargs))
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                if key in data: return data[key]
            except (FileNotFoundError, json.JSONDecodeError): data = {}
            
            result = func(*args, **kwargs)
            data[key] = result
            with open(filepath, 'w') as f:
                json.dump(data, f)
            return result
        return wrapper
    return decorator

def flatten(iterable: Any) -> list:
    return [item for sublist in iterable for item in (flatten(sublist) if isinstance(sublist, (list, tuple)) else [sublist])]