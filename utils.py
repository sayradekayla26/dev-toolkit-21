import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1.0):
    """Decorator implementing jittered exponential backoff for resilience."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            x, attempt = 0, 0
            while attempt <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise e
                    delay = (backoff_in_seconds * (2 ** attempt)) + (random.uniform(0, 1) * x)
                    time.sleep(delay)
                    attempt += 1
                    x += 1
            return None
        return wrapper
    return decorator

@retry_with_backoff(retries=3)
def execute_network_request(task_fn: Callable, *args: Any):
    """Execution wrapper for unreliable network operations."""
    return task_fn(*args)