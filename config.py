import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self.data = defaults

    def load(self, path: str) -> None:
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            try:
                loaded = json.load(f)
                self.data.update({k: v for k, v in loaded.items() if k in self.data})
            except json.JSONDecodeError:
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def dump(self) -> Dict[str, Any]:
        return {**self.data}

# usage example for dev-toolkit-21
if __name__ == '__main__':
    cfg = ConfigLoader({'timeout': 30, 'retries': 3})
    cfg.load('settings.json')
    print(f'current timeout: {cfg.timeout}')