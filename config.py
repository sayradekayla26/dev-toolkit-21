import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, default_path: str = "defaults.json"):
        self.defaults = self._load_json(default_path)

    def _load_json(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def get(self, user_cfg: Dict[str, Any]) -> Dict[str, Any]:
        return {**self.defaults, **{k: v for k, v in user_cfg.items() if v is not None}}

    def __getitem__(self, key: str) -> Any:
        return self.defaults.get(key)

def load_app_config(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    loader = ConfigLoader()
    return loader.get(overrides or {})

if __name__ == "__main__":
    base = {"host": "localhost", "port": 8080, "debug": False}
    with open("defaults.json", "w") as f:
        json.dump(base, f)
    
    c = load_app_config({"debug": True, "port": None})
    print(f"Active config: {c}")