"""Data processing pipeline using pipe-operator composition."""

from typing import Callable, Any, Generator, Iterable, TypeVar, Generic

T = TypeVar("T")
R = TypeVar("R")


class PipeStep(Generic[T, R]):
    """Encapsulates a processing step that can be chained using the OR operator."""

    def __init__(self, func: Callable[[T], R]) -> None:
        """Initialize a step with a transformer function."""
        self.func: Callable[[T], R] = func

    def __or__(self, next_step: "PipeStep[R, Any]") -> "PipeStep[T, Any]":
        """Compose two pipe steps into a single combined pipeline step."""
        return PipeStep(lambda x: next_step.func(self.func(x)))

    def __call__(self, data: T) -> R:
        """Execute the step on the given input data."""
        return self.func(data)


class BatchProcessor(Generic[T, R]):
    """Processes an iterable stream through composed pipe steps."""

    def __init__(self, pipeline: PipeStep[T, R]) -> None:
        """Bind a processing pipeline to the batch processor instance."""
        self.pipeline: PipeStep[T, R] = pipeline

    def process_stream(self, stream: Iterable[T]) -> Generator[R, None, None]:
        """Apply pipeline transformation to every element in an iterable stream."""
        for item in stream:
            yield self.pipeline(item)


def create_step(transform: Callable[[T], R]) -> PipeStep[T, R]:
    """Factory function to wrap a transformation callable into a PipeStep."""
    return PipeStep(transform)
