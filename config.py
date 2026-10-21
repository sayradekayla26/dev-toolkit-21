import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = 'APP_'):
        self._data = defaults.copy()
        self._env_prefix = env_prefix
        self._load_from_env()

    def _load_from_env(self) -> None:
        for key in self._data:
            env_val = os.getenv(f"{self._env_prefix}{key.upper()}")
            if env_val is not None:
                try:
                    self._data[key] = json.loads(env_val)
                except (json.JSONDecodeError, TypeError):
                    self._data[key] = env_val

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @classmethod
    def from_json(cls, filepath: str, defaults: Dict[str, Any]) -> 'ConfigLoader':
        instance = cls(defaults)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                file_data = json.load(f)
                instance._data.update(file_data)
                instance._load_from_env()
        return instance