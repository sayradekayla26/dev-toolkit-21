import math
import functools
from typing import Callable, Any, Dict, Type, Optional

class EdgeGuardSentinel:
    """Sentinel marker indicating an intercepted edge-case fallback value."""
    def __init__(self, original_exc: Exception, context: str):
        self.error = original_exc
        self.context = context
        
    def __repr__(self) -> str:
        return f"<EdgeGuardRecovered: {type(self.error).__name__} in '{self.context}'>"


class EdgeGuard:
    """Defensive executor mapping runtime anomalies to safe context defaults."""

    EDGE_FALLBACKS: Dict[Type[BaseException], Callable[[BaseException], Any]] = {
        ZeroDivisionError: lambda e: float('nan'),
        OverflowError: lambda e: float('inf'),
        RecursionError: lambda e: None,
        KeyError: lambda e: None,
        ValueError: lambda e: None,
        TypeError: lambda e: EdgeGuardSentinel(e, "type_mismatch")
    }

    def __init__(self, strict: bool = False, custom_fallbacks: Optional[Dict[Type[BaseException], Any]] = None):
        self.strict = strict
        self.fallbacks = dict(self.EDGE_FALLBACKS)
        if custom_fallbacks:
            for exc_type, handler in custom_fallbacks.items():
                self.fallbacks[exc_type] = handler if callable(handler) else (lambda e, h=handler: h)

    def __call__(self, fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                res = fn(*args, **kwargs)
                if isinstance(res, float) and math.isnan(res) and not self.strict:
                    return EdgeGuardSentinel(ValueError("NaN value generated"), fn.__name__)
                return res
            except BaseException as exc:
                exc_type = type(exc)
                for target_type, handler in self.fallbacks.items():
                    if issubclass(exc_type, target_type):
                        return handler(exc)
                if not self.strict:
                    return EdgeGuardSentinel(exc, fn.__name__)
                raise exc
        return wrapper

    def execute(self, fn: Callable, *args: Any, **kwargs: Any) -> Any:
        return self(fn)(*args, **kwargs)


guard = EdgeGuard()

def safe_evaluate(fn: Callable, *args: Any, **kwargs: Any) -> Any:
    return guard.execute(fn, *args, **kwargs)
