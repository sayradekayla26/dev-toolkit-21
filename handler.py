from typing import Any, Callable, Dict, Generator, List, Union
from functools import reduce


class DataStream:
    """A fluid, operator-driven wrapper for querying and reshaping nested data structures."""

    def __init__(self, data: Any):
        self._data = data

    def _walk(self, node: Any, path: tuple = ()) -> Generator[tuple[tuple, Any], None, None]:
        if isinstance(node, dict):
            for key, val in node.items():
                yield from self._walk(val, path + (key,))
        elif isinstance(node, (list, tuple)):
            for idx, val in enumerate(node):
                yield from self._walk(val, path + (idx,))
        else:
            yield path, node

    def flatten(self, separator: str = ".") -> Dict[str, Any]:
        """Flattens any nested dictionary or list into single-depth key paths."""
        return {separator.join(map(str, path)): val for path, val in self._walk(self._data)}

    def transform_leafs(self, mapper: Callable[[Any], Any]) -> Any:
        """Recursively transforms all leaf values through a mapping function."""
        def _apply(node: Any) -> Any:
            if isinstance(node, dict):
                return {k: _apply(v) for k, v in node.items()}
            if isinstance(node, list):
                return [_apply(v) for v in node]
            return mapper(node)
        return _apply(self._data)

    def filter_paths(self, predicate: Callable[[tuple, Any], bool]) -> Dict[str, Any]:
        """Selects key paths that satisfy the predicate callback."""
        return {
            ".".join(map(str, path)): val
            for path, val in self._walk(self._data)
            if predicate(path, val)
        }

    def __rshift__(self, func: Callable[[Any], Any]) -> "DataStream":
        """Enables pipeline composition via the right-shift bitwise operator."""
        return DataStream(func(self._data))

    def unwrap(self) -> Any:
        """Returns the internal payload after processing."""
        return self._data


def process_payload(data: Any, *transforms: Callable[[Any], Any]) -> Any:
    """Pipeline entry point to execute functional pipelines over generic data."""
    stream = DataStream(data)
    for transform in transforms:
        stream = stream >> transform
    return stream.unwrap()
