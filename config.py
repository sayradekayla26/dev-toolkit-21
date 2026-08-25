import json
import os
from typing import Any, Dict, Union

class ConfigError(Exception):
    pass

class Config:
    def __init__(self, source: Union[str, Dict[str, Any]]) -> None:
        self.data: Dict[str, Any] = {}
        if isinstance(source, str):
            self._load_from_file(source)
        elif isinstance(source, dict):
            self.data = dict(source)
        else:
            raise ConfigError("Source must be str or dict")

    def _load_from_file(self, filepath: str) -> None:
        if not isinstance(filepath, str) or not filepath:
            raise ConfigError("Filepath must be non-empty string")
        if not os.path.exists(filepath):
            raise ConfigError(f"File does not exist: {filepath}")
        if not os.path.isfile(filepath):
            raise ConfigError(f"Path is not a file: {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content.strip()) == 0:
                raise ConfigError("Config file is empty")
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise ConfigError("Config must be a JSON object")
            self.data = parsed
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON format: {exc}") from exc
        except PermissionError:
            raise ConfigError("Cannot read file due to permissions")
        except OSError as exc:
            raise ConfigError(f"File system error: {exc}") from exc

    def get(self, key: str, default: Any = None) -> Any:
        if not isinstance(key, str) or not key:
            raise ConfigError("Key must be non-empty string")
        try:
            current: Any = self.data
            for segment in key.split("."):
                if not isinstance(current, dict):
                    return default
                if segment not in current:
                    return default
                current = current[segment]
            return current
        except Exception as exc:
            raise ConfigError(f"Retrieval failed for key {key}") from exc

    def set(self, key: str, value: Any) -> None:
        if not isinstance(key, str) or not key:
            raise ConfigError("Key must be non-empty string")
        keys = key.split(".")
        current = self.data
        for k in keys[:-1]:
            if k not in current or not isinstance(current.get(k), dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def save(self, filepath: str) -> None:
        if not isinstance(filepath, str) or not filepath:
            raise ConfigError("Filepath must be non-empty string")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except PermissionError:
            raise ConfigError("Write permission denied")
        except OSError as exc:
            raise ConfigError(f"Save operation failed: {exc}") from exc