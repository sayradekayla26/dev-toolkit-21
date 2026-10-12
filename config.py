import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    pass

def get_env_variable(key: str, default: Any = None, required: bool = False) -> Any:
    try:
        value = os.environ.get(key, default)
        if required and value is None:
            raise ConfigError(f"Missing critical config: {key}")
        return value
    except Exception as e:
        logging.error(f"Critical failure accessing {key}: {e}")
        raise ConfigError(f"Configuration fetch failed for {key}") from e

def load_app_config() -> Dict[str, Any]:
    config = {
        "port": int(get_env_variable("APP_PORT", 8080)),
        "debug": get_env_variable("DEBUG", "false").lower() == "true",
        "secret": get_env_variable("APP_SECRET", required=True)
    }
    return config

def validate_schema(data: Dict[str, Any]) -> bool:
    required_keys = {"port", "secret"}
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)

if __name__ == "__main__":
    try:
        current_config = load_app_config()
        print(f"Config loaded: {current_config.keys()}")
    except ConfigError as err:
        print(f"System halt: {err}")