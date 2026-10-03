import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                self._recursive_update(self._data, file_data)

    def _recursive_update(self, target: Dict, source: Dict) -> None:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._recursive_update(target[key], value)
            else:
                target[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        val = self._data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

def get_config(defaults: Dict = None) -> ConfigLoader:
    return ConfigLoader(defaults or {})