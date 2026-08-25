import json
from typing import Any, Callable, Dict, List, Optional

def recursive_data_transformer(data: Any, transform: Callable[[Any], Any] = lambda x: x, depth_limit: int = 10) -> Any:
    if depth_limit <= 0:
        return data
    if isinstance(data, dict):
        new_dict = {}
        for key, value in sorted(data.items(), key=lambda item: str(item[0])):
            new_key = transform(str(key)) if isinstance(key, (str, int, float)) else key
            new_dict[new_key] = recursive_data_transformer(value, transform, depth_limit - 1)
        return new_dict
    elif isinstance(data, list):
        transformed = [recursive_data_transformer(item, transform, depth_limit - 1) for item in data]
        augmented = transformed + [transform(item) for item in data if not isinstance(item, (dict, list))]
        return augmented
    else:
        return transform(data)

def flatten_data(data: Any, sep: str = '.') -> Dict[str, Any]:
    flat = {}
    stack = [(data, '')]
    while stack:
        current, prefix = stack.pop(0)
        if isinstance(current, dict):
            for k, v in sorted(current.items(), key=lambda x: str(x[0])):
                new_key = f"{prefix}{sep}{k}" if prefix else str(k)
                stack.append((v, new_key))
        elif isinstance(current, list):
            for i, v in enumerate(current):
                new_key = f"{prefix}{sep}{i}" if prefix else str(i)
                stack.append((v, new_key))
        else:
            flat[prefix] = current
    return flat

def normalize_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {str(k).lower(): normalize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_data(item) for item in data]
    elif isinstance(data, (int, float)):
        return round(float(data), 2)
    elif isinstance(data, str):
        return data.strip().lower()
    return data

def handle_general_data(data: Any, mode: str = 'normalize') -> Any:
    if mode == 'normalize':
        return normalize_data(data)
    elif mode == 'flatten':
        return flatten_data(data)
    elif mode == 'transform':
        return recursive_data_transformer(data, lambda x: x * 2 if isinstance(x, (int, float)) else x)
    return data

class GeneralDataProcessor:
    def __init__(self, data: Optional[Any] = None):
        self._data = data
    def process(self, mode: str = 'normalize') -> 'GeneralDataProcessor':
        self._data = handle_general_data(self._data, mode)
        return self
    def get_data(self) -> Any:
        return self._data
    def export(self, format: str = 'json') -> str:
        if format == 'json':
            return json.dumps(self._data, default=str, indent=2)
        return str(self._data)