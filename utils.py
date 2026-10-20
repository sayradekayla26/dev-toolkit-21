from typing import Any, Callable, Dict, List, Union
from functools import reduce
import operator

def deep_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Dynamic path traversal using dictionary keys."""
    try:
        return reduce(operator.getitem, path.split('.'), data)
    except (KeyError, TypeError, AttributeError):
        return default

def batch_process(items: List[Any], chunk_size: int = 10) -> List[List[Any]]:
    """Generator-like slicing for memory efficiency."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def sanitize_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive dictionary key normalization to snake_case."""
    sanitized = {}
    for k, v in data.items():
        new_key = k.strip().lower().replace(' ', '_')
        if isinstance(v, dict):
            sanitized[new_key] = sanitize_keys(v)
        elif isinstance(v, list):
            sanitized[new_key] = [sanitize_keys(i) if isinstance(i, dict) else i for i in v]
        else:
            sanitized[new_key] = v
    return sanitized

def chain_ops(value: Any, ops: List[Callable]) -> Any:
    """Functional application of transformation pipelines."""
    for op in ops:
        value = op(value)
    return value