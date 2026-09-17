import time
import functools
from typing import Callable, Type, Tuple, Any, Union

class ChaoticBackoff:
    """Generates deterministic pseudo-random delays using a chaotic logistic map."""
    def __init__(self, base_delay: float = 1.0, chaos_factor: float = 3.9):
        self.base = base_delay
        self.r = chaos_factor
        self.x = 0.35

    def next_delay(self, attempt: int) -> float:
        self.x = self.r * self.x * (1.0 - self.x)
        exponential_part = self.base * (1.618 ** attempt)
        jitter = self.x * self.base
        return exponential_part + jitter

def retry_on_failure(
    exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = Exception,
    max_attempts: int = 4,
    base_delay: float = 0.5
) -> Callable:
    """Decorator applying chaotic golden-ratio backoff retry logic to operations."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff = ChaoticBackoff(base_delay=base_delay)
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt >= max_attempts:
                        raise err
                    delay = backoff.next_delay(attempt)
                    time.sleep(delay)
        return wrapper
    return decorator