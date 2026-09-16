import os
import json
from collections import ChainMap
from typing import Any, Dict, Union, Optional
from pathlib import Path


class ConfigLoader(dict):
    """Cascading configuration loader with env and default fallbacks."""

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, env_prefix: str = "APP_"):
        super().__init__()
        self._defaults = defaults or {}
        self._env_prefix = env_prefix
        self._env_map: Dict[str, Any] = {}
        self._chain = ChainMap(self, self._env_map, self._defaults)
        self._sync_env()

    def _sync_env(self) -> None:
        for key, val in os.environ.items():
            if key.startswith(self._env_prefix):
                clean_key = key[len(self._env_prefix) :].lower()
                self._env_map[clean_key] = self._cast_value(val)

    @staticmethod
    def _cast_value(val: str) -> Union[int, float, bool, str]:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        for cast in (int, float):
            try:
                return cast(val)
            except ValueError:
                pass
        return val

    def load_file(self, filepath: Union[str, Path]) -> "ConfigLoader":
        path = Path(filepath)
        if path.is_file() and path.suffix in (".json", ".js"):
            with open(path, "r", encoding="utf-8") as f:
                self.update(json.load(f))
        return self

    def __getitem__(self, item: str) -> Any:
        try:
            return self._chain[item]
        except KeyError:
            raise KeyError(f"Configuration key '{item}' not found") from None

    def get(self, key: str, default: Any = None) -> Any:
        return self._chain.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._chain:
            return self._chain[name]
        raise AttributeError(f"Configuration key '{name}' does not exist")
