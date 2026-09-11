import sys
import functools
from typing import Any, Callable

class InternedRegistry:
    """High-performance attribute access via key interning."""
    __slots__ = ('_cache',)

    def __init__(self):
        self._cache = {}

    def __getattr__(self, name: str) -> Any:
        if name not in self._cache:
            self._cache[name] = sys.intern(name)
        return self._cache[name]

class ConfigStore:
    """Pre-computed bitmasks for hot path logic."""
    READ_BIT = 1 << 0
    WRITE_BIT = 1 << 1
    EXECUTE_BIT = 1 << 2
    AUTH_MASK = READ_BIT | WRITE_BIT | EXECUTE_BIT

    def __init__(self):
        self.registry = InternedRegistry()

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def get_permission_flags(mode: int) -> dict:
        return {
            "read": bool(mode & ConfigStore.READ_BIT),
            "write": bool(mode & ConfigStore.WRITE_BIT),
            "execute": bool(mode & ConfigStore.EXECUTE_BIT)
        }

def memoized_property(func: Callable) -> property:
    """Custom property caching for compute-heavy constants."""
    cache_name = f"__{func.__name__}_cache"
    def wrapper(self):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, func(self))
        return getattr(self, cache_name)
    return property(wrapper)

GLOBAL_STORE = ConfigStore()