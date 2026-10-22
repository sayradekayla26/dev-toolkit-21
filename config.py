import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = 'APP_'):
        self._data = defaults.copy()
        self._env_prefix = env_prefix

    def load(self, filepath: str = 'config.json') -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                self._data.update(file_data)
        self._apply_env_overrides()
        return self

    def _apply_env_overrides(self):
        for key in self._data.keys():
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                try:
                    self._data[key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    self._data[key] = val

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute {name}")

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults).load()