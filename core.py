import functools
import time
from typing import Callable, Any, Dict

class Memoizer:
    def __init__(self, ttl: int = 60):
        self.cache: Dict[tuple, tuple] = {}
        self.ttl = ttl

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def heavy_computation(x: int) -> int:
    time.sleep(1)
    return x * x

@Memoizer(ttl=300)
def cached_processor(data: int) -> int:
    return heavy_computation(data)

class PerformanceOptimizer:
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    def optimize(self, func: Callable) -> Callable:
        def decorated(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            res = func(*args, **kwargs)
            duration = time.perf_counter() - start
            if duration > self.threshold:
                print(f'Warning: {func.__name__} took {duration:.4f}s')
            return res
        return decorated