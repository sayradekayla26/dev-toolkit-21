from typing import Any, Callable, Dict, List, Union
from functools import reduce
import operator

class DataFlow:
    def __init__(self, data: Any):
        self._data = data

    def __getitem__(self, key: str) -> 'DataFlow':
        try:
            return DataFlow(self._data[key])
        except (KeyError, TypeError, IndexError):
            return DataFlow(None)

    def get(self) -> Any:
        return self._data

    def apply(self, func: Callable[[Any], Any]) -> 'DataFlow':
        return DataFlow(func(self._data)) if self._data is not None else self

def deep_reach(data: Dict, path: str, delimiter: str = '.') -> Any:
    """Extract nested value using dot-notation or custom delimiter."""
    keys = path.split(delimiter)
    return reduce(lambda d, k: d.get(k) if isinstance(d, dict) else None, keys, data)

def sanitize_stream(stream: List[Dict], keys: List[str]) -> List[Dict]:
    """Filtering of data dictionaries against provided keys."""
    return [{k: v for k, v in item.items() if k in keys} for item in stream]

def recursive_map(data: Any, transformer: Callable[[Any], Any]) -> Any:
    """Recursive tree transformation using custom function."""
    if isinstance(data, dict):
        return {k: recursive_map(v, transformer) for k, v in data.items()}
    if isinstance(data, list):
        return [recursive_map(i, transformer) for i in data]
    return transformer(data)