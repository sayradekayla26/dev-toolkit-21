import functools
from typing import Any, Callable

class ValidationError(Exception):
    """Custom exception for toolkit input violations."""
    pass

def validate_payload(schema: dict):
    """Decorator injecting runtime sanity checks into processing loop."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = kwargs.get('data') or (args[0] if args else {})
            for key, expected_type in schema.items():
                val = data.get(key)
                if val is None or not isinstance(val, expected_type):
                    raise ValidationError(f"field '{key}' expected {expected_type.__name__}, got {type(val).__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def secure_loop(processor: Callable):
    """High-order wrapper for iterative data pipelines."""
    def executor(data_stream):
        for entry in data_stream:
            try:
                processor(data=entry)
            except ValidationError as e:
                print(f"[!] Integrity violation: {e}")
                continue
    return executor