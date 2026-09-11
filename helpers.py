import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic dictionary proxy for configuration defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load_from_env(self, prefix: str = "APP_") -> None:
        for key in self._data:
            env_key = f"{prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                self._data[key] = int(val) if val.isdigit() else val

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

    @property
    def settings(self) -> Dict[str, Any]:
        return self._data.copy()

# Usage example:
# cfg = ConfigLoader({'port': 8080, 'debug': False})
# cfg.load_from_env()
# print(cfg['port'])