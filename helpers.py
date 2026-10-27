import functools
import collections
from typing import Any, Callable, TypeVar, Iterable

T = TypeVar('T')

class DataPipeline:
    """A whimsical data processing chain wrapper."""
    def __init__(self, data: Iterable[T]):
        self._data = list(data)

    def transform(self, func: Callable[[T], Any]) -> 'DataPipeline':
        self._data = [func(item) for item in self._data]
        return self

    def collect(self) -> list[Any]:
        return self._data

def deep_flatten(nested: Iterable) -> list:
    """Recursively unpack nested structures using recursion."""
    result = []
    for item in nested:
        if isinstance(item, (list, tuple, set)):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def batch_process(items: Iterable[T], size: int = 10) -> Iterable[list[T]]:
    """Yields non-overlapping chunks from a stream."""
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def smart_dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """Merges dicts, concatenating values if keys collide."""
    result = collections.defaultdict(list)
    for d in dicts:
        for k, v in d.items():
            result[k].append(v)
    return {k: v[0] if len(v) == 1 else v for k, v in result.items()}