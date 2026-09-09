import sys
import time
from typing import Any, Callable, Dict, Type

class ToolkitError(Exception):
    """Base exception with dynamic payload tracking and self-inspection capabilities."""
    def __init__(self, message: str, payload: Dict[str, Any] = None):
        super().__init__(message)
        self.payload = payload or {}
        self.timestamp = time.time()

class DynamicFallbackError(ToolkitError):
    """Raised when an operation fails, packaging a deferred recovery strategy."""
    def __init__(self, message: str, recovery_callable: Callable[[], Any], payload: Dict[str, Any] = None):
        super().__init__(message, payload)
        self.recover = recovery_callable

class EdgeCaseMitigator:
    """Context manager to intercept exceptions and deploy custom fallback mechanics."""
    def __init__(self, fallback_map: Dict[Type[BaseException], Callable[[BaseException], Any]]):
        self.fallback_map = fallback_map
        self.last_handled_exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False

        for target_type, fallback in self.fallback_map.items():
            if issubclass(exc_type, target_type):
                try:
                    fallback(exc_val)
                    self.last_handled_exception = exc_val
                    return True
                except Exception as cascade_error:
                    raise DynamicFallbackError(
                        f"Fallback resolution crashed: {cascade_error}",
                        recovery_callable=lambda: None,
                        payload={"original_error": exc_val, "cascade_error": cascade_error}
                    ) from exc_val
        return False