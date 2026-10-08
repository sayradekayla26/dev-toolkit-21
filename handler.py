import time
import functools
import random

def retry_operation(max_attempts=3, backoff_factor=1.5, exceptions=(ConnectionError, TimeoutError)):
    """ decorator for resilient network requests """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = 1.0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff_factor
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def fetch_remote_resource(url):
    # simulation of unpredictable network behavior
    if random.random() < 0.7:
        raise ConnectionError(f"transient failure at {url}")
    return {"status": 200, "data": "success"}