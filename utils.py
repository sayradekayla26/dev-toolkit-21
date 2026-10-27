from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
import json

def cast_data(data: Any, target_type: type) -> Any:
    try:
        return target_type(data)
    except (ValueError, TypeError):
        return None

def deep_flatten(obj: Union[Dict, List]) -> List[Any]:
    items = []
    container = obj.values() if isinstance(obj, dict) else obj
    for i in container:
        if isinstance(i, (dict, list)):
            items.extend(deep_flatten(i))
        else:
            items.append(i)
    return items

def safe_access(data: Dict, path: str, default: Any = None) -> Any:
    keys = path.split('.')
    current = data
    try:
        for key in keys:
            current = current[key]
        return current if current is not None else default
    except (KeyError, TypeError):
        return default

def pipeline(data: Any, *funcs: Callable) -> Any:
    result = data
    for func in funcs:
        result = func(result)
    return result

def sanitize_json(data: Any) -> str:
    return json.dumps(data, default=str, indent=2)

class DataWrapper:
    def __init__(self, data: Any):
        self._data = data
    def map(self, func: Callable) -> 'DataWrapper':
        return DataWrapper(func(self._data))
    def get(self) -> Any:
        return self._data