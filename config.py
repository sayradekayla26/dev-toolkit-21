import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A configuration loader that resolves defaults via object attribute access."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load_env(self, prefix: str = "APP_") -> None:
        for key in self._data.keys():
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._data[key] = self._cast(env_val)

    def load_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def _cast(self, val: str) -> Any:
        if val.lower() in ('true', 'yes'): return True
        if val.lower() in ('false', 'no'): return False
        try: return int(val)
        except ValueError:
            try: return float(val)
            except ValueError: return val

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config key '{name}' not found")

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self._data.keys())}>"