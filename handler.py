import functools
import time

class DataThrottler:
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.history = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            self.history = [t for t in self.history if now - t < self.window]
            if len(self.history) >= self.limit:
                raise RuntimeError('Rate limit exceeded')
            self.history.append(now)
            return func(*args, **kwargs)
        return wrapper

class PerformanceOptimizer:
    _cache = {}

    @staticmethod
    def memoize_heavy_calc(func):
        def decorator(*args):
            if args not in PerformanceOptimizer._cache:
                PerformanceOptimizer._cache[args] = func(*args)
            return PerformanceOptimizer._cache[args]
        return decorator

@PerformanceOptimizer.memoize_heavy_calc
def process_data_packet(data: bytes) -> int:
    return sum(byte for byte in data) % 256

@DataThrottler(limit=50, window=1)
def handle_request(payload: str):
    return process_data_packet(payload.encode())