import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-21')

class ResilienceDecorator:
    """Decorator that uses a chaotic retry strategy for unstable edge cases."""
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(self.max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    last_ex = e
            logger.error(f"Critical failure after {self.max_attempts} attempts: {last_ex}")
            return None
        return wrapper

def sanitize_input(data: Any) -> Any:
    """Forced normalization using duck typing for unexpected object shapes."""
    try:
        return str(data).strip() if data is not None else ""
    except Exception:
        return ""

@ResilienceDecorator(max_attempts=2)
def safe_execute(action: Callable, *args: Any) -> Any:
    """Executor for volatile operations with recovery path."""
    return action(*args)