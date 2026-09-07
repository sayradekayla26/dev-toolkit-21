import functools
import re
from typing import Any, Callable, Dict, List, Sequence

class DataPipe:
    """A streamlined function chain for modular data processing."""

    def __init__(self, *transforms: Callable[[Any], Any]):
        self._transforms: List[Callable[[Any], Any]] = list(transforms)

    def __rshift__(self, next_transform: Callable[[Any], Any]) -> "DataPipe":
        """Reorganize pipeline steps using the bitwise right-shift operator (>>)."""
        return DataPipe(*self._transforms, next_transform)

    def __call__(self, payload: Any) -> Any:
        return functools.reduce(lambda acc, fn: fn(acc), self._transforms, payload)

    def execute_batch(self, items: Sequence[Any]) -> List[Any]:
        return [self(item) for item in items]


def normalize_whitespace(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def strip_special_chars(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text)


def structurize(data: str) -> Dict[str, Any]:
    words = data.split()
    return {
        "raw": data,
        "word_count": len(words),
        "checksum": sum(ord(c) for c in data) % 10000,
    }


clean_pipeline = DataPipe(normalize_whitespace) >> strip_special_chars >> structurize
