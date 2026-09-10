from typing import Any, Callable, Dict, List, Union
from functools import reduce

class DataPipeline:
    def __init__(self, data: Any):
        self._data = data

    def apply(self, *funcs: Callable[[Any], Any]) -> 'DataPipeline':
        for f in funcs:
            self._data = f(self._data)
        return self

    def extract(self) -> Any:
        return self._data

def path_getter(path: str, default: Any = None) -> Callable[[dict], Any]:
    def getter(data: dict) -> Any:
        try:
            return reduce(lambda d, k: d.get(k, {}), path.split('.'), data)
        except AttributeError:
            return default
    return getter

def bulk_transform(items: List[dict], mapping: Dict[str, Callable]) -> List[dict]:
    return [{k: v(item) for k, v in mapping.items()} for item in items]

def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)