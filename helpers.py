import functools
from typing import Any, Callable, Dict, List, Type

class InputValidationError(Exception):
    pass

def validate_payload(schema: Dict[str, Type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = kwargs.get('data') or (args[0] if args else {})
            for key, expected_type in schema.items():
                val = data.get(key)
                if val is None or not isinstance(val, expected_type):
                    raise InputValidationError(f'invalid field: {key}, expected {expected_type.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def process_stream(items: List[dict], processor: Callable):
    processed = []
    for item in items:
        try:
            result = processor(data=item)
            processed.append(result)
        except InputValidationError as e:
            print(f'skipping record due to: {e}')
    return processed

def sanitize_input(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        clean = {k: str(v).strip() for k, v in kwargs.get('data', {}).items()}
        return func(*args, data=clean)
    return wrapper