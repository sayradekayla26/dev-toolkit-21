import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1.0):
    """decorator for exponential backoff network retries"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=3)
def fetch_remote_resource(url):
    # simulated network interaction logic
    if random.random() < 0.7:
        raise ConnectionError(f"failed to reach {url}")
    return f"data from {url}"