import time
import functools
import random
from typing import Callable, Any

def retry_request(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * base_delay)
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + jitter
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def network_validator(func: Callable) -> Callable:
    @functools.wraps(func)
    def sanity_check(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise ValueError("Empty network response detected")
        return result
    return sanity_check