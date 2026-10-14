import json
from functools import wraps
from typing import Any, Callable

def deep_flatten(lst: list) -> list:
    flat = []
    for item in lst:
        if isinstance(item, list):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def safe_json_load(data: str, fallback: Any = None) -> Any:
    try:
        return json.loads(data)
    except (ValueError, TypeError):
        return fallback

def time_execution(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'[perf] {func.__name__} took {end - start:.4f}s')
        return result
    return wrapper

class DataPipeline:
    def __init__(self, processors: list = None):
        self.processors = processors or []

    def run(self, initial_data: Any) -> Any:
        result = initial_data
        for p in self.processors:
            result = p(result)
        return result

def compose(*funcs):
    return lambda x: (lambda v, f: f(v))(x, funcs[-1]) if not funcs else compose(*funcs[:-1])(funcs[-1](x))