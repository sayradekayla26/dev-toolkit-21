from collections.abc import Mapping, Sequence
from typing import Any, Callable, Generator


class DataPipe:
    """A flexible node transformer for nested data structures with path querying."""

    def __init__(self, data: Any):
        self._data = data

    def extract(self, path: str, default: Any = None) -> Any:
        """Extract nested key using dot notation, supporting list index wildcards."""
        keys = path.split(".")
        current = self._data

        for idx, key in enumerate(keys):
            if isinstance(current, Mapping) and key in current:
                current = current[key]
            elif isinstance(current, Sequence) and not isinstance(current, (str, bytes)):
                if key == "*":
                    remaining = ".".join(keys[idx + 1:])
                    return [DataPipe(item).extract(remaining, default) for item in current]
                if key.isdigit() and int(key) < len(current):
                    current = current[int(key)]
                else:
                    return default
            else:
                return default
        return current

    def reshape(self, template: dict[str, str | Callable[[Any], Any]]) -> dict[str, Any]:
        """Reshape data according to a template mapping target keys to paths or lambdas."""
        result = {}
        for target_key, source in template.items():
            if callable(source):
                result[target_key] = source(self._data)
            elif isinstance(source, str):
                result[target_key] = self.extract(source)
            else:
                result[target_key] = source
        return result

    def stream_nodes(self) -> Generator[tuple[str, Any], None, None]:
        """Yield all leaf nodes as path-value tuples."""
        def _walk(obj: Any, prefix: str) -> Generator[tuple[str, Any], None, None]:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    yield from _walk(v, f"{prefix}.{k}" if prefix else str(k))
            elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
                for i, item in enumerate(obj):
                    yield from _walk(item, f"{prefix}.{i}")
            else:
                yield prefix, obj

        yield from _walk(self._data, "")


def morph_structure(data: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """Utility wrapper for quick structural morphing of nested data."""
    return DataPipe(data).reshape(schema)
