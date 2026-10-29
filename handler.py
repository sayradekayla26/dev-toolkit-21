"""Monadic event handler supporting pipeline composition using custom operators."""

from typing import TypeVar, Callable, Generic, Any, List, Optional

T = TypeVar("T")
R = TypeVar("R")
S = TypeVar("S")


class PipelineHandler(Generic[T, R]):
    """Callable container that enables step-wise functional chaining using '>>'."""

    def __init__(self, func: Callable[[T], R]) -> None:
        """Wrap a standard function into a chainable handler step."""
        self._func: Callable[[T], R] = func

    def __call__(self, payload: T) -> R:
        """Execute the underlying processing block on input payload."""
        return self._func(payload)

    def __rshift__(self, next_handler: "PipelineHandler[R, S]") -> "PipelineHandler[T, S]":
        """Compose current handler with another handler in left-to-right sequence."""
        def composed(data: T) -> S:
            return next_handler(self._func(data))
        return PipelineHandler(composed)


class EventDispatcher:
    """Registry and execution manager for event handling pipelines."""

    def __init__(self) -> None:
        """Initialize empty dispatch routes."""
        self._routes: dict[str, PipelineHandler[Any, Any]] = {}

    def register(self, event_type: str, handler: PipelineHandler[Any, Any]) -> None:
        """Map an event topic to a composite execution pipeline."""
        self._routes[event_type] = handler

    def dispatch(self, event_type: str, payload: Any) -> Optional[Any]:
        """Trigger execution flow for registered event type if present."""
        handler = self._routes.get(event_type)
        return handler(payload) if handler else None


# Pre-configured pipeline helpers
clean_str = PipelineHandler(lambda val: str(val).strip().lower())
split_words = PipelineHandler(lambda text: text.split())
unique_words = PipelineHandler(lambda items: sorted(list(set(items))))

# Standard text processing pipeline
text_pipeline: PipelineHandler[Any, List[str]] = clean_str >> split_words >> unique_words
