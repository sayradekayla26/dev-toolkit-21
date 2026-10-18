from typing import List, Callable, Any, TypeVar

T = TypeVar('T')

class DataTransformer:
    """A whimsical pipeline for list-based data mutation."""

    def __init__(self, sequence: List[T]) -> None:
        """Initialize with a list and internal mutation state."""
        self._buffer: List[T] = sequence

    def apply(self, func: Callable[[T], T]) -> 'DataTransformer':
        """Map a function over the buffer and return self for chaining."""
        self._buffer = [func(item) for item in self._buffer]
        return self

    def reduce(self, initial: T, operation: Callable[[T, T], T]) -> T:
        """Fold the sequence using a provided reduction logic."""
        result: T = initial
        for item in self._buffer:
            result = operation(result, item)
        return result

    @property
    def current_state(self) -> List[T]:
        """Export the current buffer status."""
        return self._buffer

def run_pipeline(data: List[int]) -> int:
    """Execute a sequence of transformations and sum result."""
    transformer = DataTransformer(data)
    return transformer.apply(lambda x: x * 2).reduce(0, lambda a, b: a + b)

if __name__ == '__main__':
    print(f"Final result: {run_pipeline([1, 2, 3, 4])}")