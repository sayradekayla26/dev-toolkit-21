from typing import Any, Callable, Generic, TypeVar, Union

T = TypeVar("T")
R = TypeVar("R")

class Pipeline(Generic[T]):
    """A monadic-ish wrapper to chain operations via the shift operator.

    Allows sequential application of callables using '>>' syntactical sugar.
    """

    def __init__(self, value: T) -> None:
        self.value: T = value

    def __rshift__(self, func: Callable[[T], R]) -> "Pipeline[R]":
        """Applies func to the internal value, wrapping the result in Pipeline."""
        return Pipeline(func(self.value))

    def __repr__(self) -> str:
        return f"Pipeline({self.value!r})"


def safe_lookup(source: Union[dict, list], path: str, fallback: Any = None) -> Any:
    """Query deeply nested structures using a dotted path string.

    Supports dict keys and list indices (if the path segment is numeric).
    """
    current: Any = source
    for step in path.split("."):
        try:
            if isinstance(current, dict):
                current = current[step]
            elif isinstance(current, list) and step.isdigit():
                current = current[int(step)]
            else:
                return fallback
        except (KeyError, IndexError, TypeError):
            return fallback
    return current