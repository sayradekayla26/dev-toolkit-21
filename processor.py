import functools
from typing import Callable, Any, Dict, Tuple


class AdaptiveMemoizer:
    """Adaptive dynamic memoizer with bitwise access frequency decay."""

    __slots__ = ("_cache", "_freq", "_maxsize", "_hits", "_misses")

    def __init__(self, maxsize: int = 256):
        self._cache: Dict[Tuple, Any] = {}
        self._freq: Dict[Tuple, int] = {}
        self._maxsize = maxsize
        self._hits = 0
        self._misses = 0

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                self._hits += 1
                self._freq[key] = (self._freq[key] >> 1) | 0x80
                return self._cache[key]

            self._misses += 1
            if len(self._cache) >= self._maxsize:
                lfu_key = min(self._freq, key=self._freq.get)
                del self._cache[lfu_key]
                del self._freq[lfu_key]

            res = func(*args, **kwargs)
            self._cache[key] = res
            self._freq[key] = 0x80
            return res

        def cache_stats():
            total = self._hits + self._misses
            ratio = (self._hits / total) if total > 0 else 0.0
            return {"hits": self._hits, "misses": self._misses, "hit_ratio": ratio}

        wrapper.stats = cache_stats
        return wrapper
