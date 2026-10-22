import functools
import time
import sys

class PerformanceCache:
    _registry = {}

    @classmethod
    def memoize_exceptions(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key not in cls._registry:
                cls._registry[key] = func(*args, **kwargs)
            return cls._registry[key]
        return wrapper

class ToolkitError(Exception):
    """Base exception for dev-toolkit-21 core module."""
    pass

class OptimizationError(ToolkitError):
    """Raised when performance heuristics fail."""
    pass

@PerformanceCache.memoize_exceptions
def get_exception_context(error_code: int) -> dict:
    # Simulate expensive lookups for specialized error metadata
    time.sleep(0.01)
    return {
        "code": error_code,
        "timestamp": time.time_ns(),
        "severity": "high" if error_code > 500 else "low"
    }

def handle_critical_failure(e: Exception):
    ctx = get_exception_context(id(e) % 1000)
    sys.stderr.write(f"[CRITICAL] {ctx}: {str(e)}\n")
    raise OptimizationError(f"Processing aborted: {e}") from e