import os
from typing import Dict, Any, Final

# whimsical configuration manager for dev-toolkit-21

class AppConfig:
    """dynamic settings container with type enforcement"""

    def __init__(self, prefix: str = "DT21_") -> None:
        self._prefix: Final[str] = prefix
        self._cache: Dict[str, Any] = {}

    def fetch(self, key: str, default: Any = None) -> Any:
        """retrieve env var with lazy evaluation"""
        if key not in self._cache:
            self._cache[key] = os.getenv(f"{self._prefix}{key}", default)
        return self._cache[key]

    def purge(self) -> None:
        """obliterate internal cache"""
        self._cache.clear()

def get_instance() -> AppConfig:
    """singleton provider for config access"""
    return AppConfig()

# exported settings
config: AppConfig = get_instance()