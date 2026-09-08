import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "APP_"):
        self.data = defaults.copy()
        self._load_from_env(env_prefix)

    def _load_from_env(self, prefix: str) -> None:
        for key in self.data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                try:
                    self.data[key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    self.data[key] = val

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"config has no attribute {name}")

    @classmethod
    def from_json(cls, path: str, defaults: Dict[str, Any]) -> 'ConfigLoader':
        instance = cls(defaults)
        if os.path.exists(path):
            with open(path, 'r') as f:
                instance.data.update(json.load(f))
        return instance