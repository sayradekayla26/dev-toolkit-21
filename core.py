import functools
import time
from typing import Callable, Any, Dict, Tuple

class AdaptiveHotPathOptimizer:
    """
    Dynamically optimizes slow, repetitive function calls by
    promoting them to a localized cache path after a profiling window.
    """
    def __init__(self, threshold_ms: float = 0.01, observation_window: int = 5):
        self.threshold_ms = threshold_ms
        self.observation_window = observation_window
        self.profiles: Dict[str, Dict[str, Any]] = {}

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        name = func.__qualname__
        self.profiles[name] = {
            "hits": 0,
            "total_duration": 0.0,
            "hot": False,
            "cache": {}
        }

        @functools.wraps(func)
        def optimized_wrapper(*args: Any, **kwargs: Any) -> Any:
            prof = self.profiles[name]
            cache_key: Tuple[Any, ...] = (args, tuple(sorted(kwargs.items())))

            if prof["hot"]:
                if cache_key in prof["cache"]:
                    return prof["cache"][cache_key]
                res = func(*args, **kwargs)
                prof["cache"][cache_key] = res
                return res

            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time

            prof["hits"] += 1
            prof["total_duration"] += elapsed

            if prof["hits"] >= self.observation_window:
                avg_duration_ms = (prof["total_duration"] / prof["hits"]) * 1000
                if avg_duration_ms > self.threshold_ms:
                    prof["hot"] = True
                    prof["cache"][cache_key] = result

            return result

        return optimized_wrapper
