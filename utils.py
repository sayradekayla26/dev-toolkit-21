import functools
import time
import collections

class memoize_with_expiry:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(data, chunk_size=100):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def fast_flatten(nested_list):
    stack = list(nested_list)
    while stack:
        item = stack.pop(0)
        if isinstance(item, list):
            stack[0:0] = item
        else:
            yield item

def adaptive_pool_size(current_load, baseline=4):
    return max(baseline, int(current_load * 1.5))

# dev-toolkit-21 core utility enhancements