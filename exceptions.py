import sys
import time
from typing import Any, Dict, Callable

class QuantumException(Exception):
    """
    An exception whose state dynamically alters based on how many times
    it has been queried, or the elapsed time since its creation.
    """
    def __init__(self, base_message: str, context: Dict[str, Any] = None):
        self.base_message = base_message
        self.context = context or {}
        self.created_at = time.time()
        self._access_count = 0
        super().__init__(self.base_message)

    @property
    def age(self) -> float:
        return time.time() - self.created_at

    def __str__(self) -> str:
        self._access_count += 1
        severity = "CRITICAL" if self._access_count > 3 else "WARNING"
        return (
            f"[{severity}] {self.base_message} (Observed x{self._access_count}, "
            f"Age: {self.age:.4f}s, Context: {self.context})"
        )

class EdgeCaseShield:
    """
    A decorator to intercept unexpected edge cases and transform them
    into QuantumExceptions with execution state capture.
    """
    def __init__(self, fallback: Any = None):
        self.fallback = fallback

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    "function": func.__name__,
                    "args_len": len(args),
                    "kwargs_keys": list(kwargs.keys()),
                    "exception_type": type(e).__name__
                }
                raise QuantumException(
                    f"Shielded execution failure inside '{func.__name__}'",
                    context=context
                ) from e
        return wrapper