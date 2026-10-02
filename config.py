import os
import json
from typing import Any, Dict

class ConfigLoader:
    """Magic config loader with cascade fallbacks"""
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_env(self, prefix: str = "APP_") -> None:
        for key, value in os.environ.items():
            if key.startswith(prefix):
                self._data[key[len(prefix):].lower()] = value

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, "r") as f:
                self._data.update(json.load(f))

    def __getattr__(self, name: str) -> Any:
        if name not in self._data:
            raise AttributeError(f"Config {name} not found")
        return self._data[name]

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

def get_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_json("config.json")
    loader.load_from_env()
    return loader