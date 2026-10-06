import time
import random
import functools
from typing import Callable, Any, Generator, Type, Tuple

def golden_backoff(base: float = 0.5, max_delay: float = 10.0) -> Generator[float, None, None]:
    """Generates backoff delays using golden ratio scaling with jitter."""
    phi = 1.61803398875
    current = base
    while True:
        jitter = random.uniform(-0.1, 0.1) * current
        yield min(max_delay, current + jitter)
        current *= phi

class NetworkRetryHandler:
    """Decorator engine for retrying volatile operations with generator-based backoff."""
    
    def __init__(
        self,
        attempts: int = 4,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        backoff_gen: Callable[[], Generator[float, None, None]] = golden_backoff
    ):
        self.attempts = attempts
        self.exceptions = exceptions
        self.backoff_gen = backoff_gen

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = self.backoff_gen()
            last_err = None
            
            for attempt in range(1, self.attempts + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as err:
                    last_err = err
                    if attempt == self.attempts:
                        break
                    delay = next(delays)
                    time.sleep(delay)
            
            raise RuntimeError(f"Operation '{func.__name__}' failed after {self.attempts} attempts") from last_err
        return wrapper

def execute_with_retry(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Utility function to execute arbitrary callable with standard golden backoff."""
    handler = NetworkRetryHandler(attempts=3)
    return handler(func)(*args, **kwargs)
