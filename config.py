import json
import os
from typing import Any, Dict, Optional
class ConfigurationLoader:
    def __init__(self, default_config: Optional[Dict[str, Any]] = None):
        self.default_config = default_config or {}
        self.config: Dict[str, Any] = self.default_config.copy()
    def load_from_dict(self, user_config: Dict[str, Any]):
        def merge(current, updates):
            for key, value in updates.items():
                if key in current and isinstance(current[key], dict) and isinstance(value, dict):
                    merge(current[key], value)
                else:
                    current[key] = value
            return current
        merge(self.config, user_config)
    def load_from_json_file(self, file_path: str):
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.load_from_dict(data)
    def load_from_env(self, prefix: str = "CONFIG_"):
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                if value.lower() in ('true', 'false'):
                    self.config[config_key] = value.lower() == 'true'
                else:
                    try:
                        self.config[config_key] = int(value)
                    except ValueError:
                        try:
                            self.config[config_key] = float(value)
                        except ValueError:
                            self.config[config_key] = value
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)
    def __getitem__(self, key: str) -> Any:
        if key in self.config:
            return self.config[key]
        raise KeyError(key)
    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value
    def to_dict(self) -> Dict[str, Any]:
        return self.config.copy()
def create_loader(defaults: Optional[Dict[str, Any]] = None) -> ConfigurationLoader:
    if defaults is None:
        defaults = {"host": "localhost", "port": 8080, "debug": False, "database": {"name": "default_db", "user": "admin"}}
    loader = ConfigurationLoader(defaults)
    loader.load_from_env()
    return loader
if __name__ == "__main__":
    loader = create_loader()
    print("Host:", loader.get("host"))
    loader.load_from_dict({"port": 9000})
    print("Port:", loader["port"])
    print("All:", loader.to_dict())