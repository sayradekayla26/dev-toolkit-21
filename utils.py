import time
import functools
import random

def retry_operation(max_attempts=3, delay=1.0, backoff=2):
    """Decorator implementing exponential backoff for network fragility."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.1 * current_delay)
                    time.sleep(sleep_time)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

@retry_operation(max_attempts=4, delay=0.5)
def fetch_remote_data(url):
    """Mock network call utilizing the retry logic."""
    if random.random() < 0.7:
        raise ConnectionError("Transient network instability detected")
    return {"status": 200, "payload": "success"}