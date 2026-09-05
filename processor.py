import time
import functools
import random

def retry_with_backoff(max_retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries == max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** retries)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
                    retries += 1
        return wrapper
    return decorator

class NetworkHandler:
    @retry_with_backoff(max_retries=3)
    def fetch_data(self, url):
        # Simulation of unstable network
        if random.random() < 0.7:
            raise ConnectionError("Transient network failure")
        return {"status": 200, "payload": "success"}

def process_stream(data_source):
    handler = NetworkHandler()
    results = []
    for item in data_source:
        try:
            results.append(handler.fetch_data(item))
        except ConnectionError:
            results.append(None)
    return results