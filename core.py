import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._config = defaults

    def load(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return self._config
        
        try:
            with open(path, 'r') as f:
                user_data = json.load(f)
                return {**self._config, **user_data}
        except (json.JSONDecodeError, IOError):
            return self._config

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __repr__(self) -> str:
        return f"Config(keys={list(self._config.keys())})"

# usage pattern
if __name__ == '__main__':
    defaults = {"host": "localhost", "port": 8080, "debug": False}
    loader = ConfigLoader(defaults)
    current_cfg = loader.load('settings.json')
    print(f"current configuration status: {current_cfg}")