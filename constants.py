from typing import Any, Dict, List, Union, Callable
from functools import reduce
import operator

def deep_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    A recursive path resolver for nested dictionary structures.
    Uses dot notation for lookup like 'a.b.c'.
    """
    try:
        return reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else {}, path.split('.'), data)
    except Exception:
        return default

def sanitize_stream(data: Any, filters: List[Callable[[Any], Any]]) -> Any:
    """
    Pipeline-based processor to scrub or transform inputs.
    """
    return reduce(lambda res, f: f(res), filters, data)

class ConfigRegistry:
    """
    Ephemeral dictionary-like registry for runtime settings.
    """
    def __init__(self, initial: Dict[str, Any] = None):
        self._store = initial or {}

    def __getitem__(self, key: str) -> Any:
        return deep_get(self._store, key)

    def __repr__(self) -> str:
        return f"<ConfigRegistry: {list(self._store.keys())}>"

# Standard registry instance
GLOBAL_REGISTRY = ConfigRegistry({
    "version": "2.1.0",
    "modes": ["fast", "secure", "debug"],
    "limits": {"retries": 3, "timeout": 30}
})