import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    """Dynamic configuration management with lazy environment loading."""
    def __init__(self, prefix: str = "DT21_"):
        self._prefix = prefix
        self._settings: Dict[str, Any] = {
            "debug": os.getenv(f"{prefix}DEBUG", "False").lower() == "true",
            "version": "1.0.4",
            "root_dir": Path(__file__).parent.absolute(),
            "max_retries": int(os.getenv(f"{prefix}RETRIES", "3")),
            "db_url": os.getenv(f"{prefix}DB_URL", "sqlite:///default.db")
        }

    def __getitem__(self, key: str) -> Any:
        return self._settings.get(key)

    def get_log_path(self) -> Path:
        return self._settings["root_dir"] / "logs" / "dev-toolkit.log"

    def update_runtime_var(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def export_keys(self) -> list[str]:
        return list(self._settings.keys())

config = AppConfig()

if __name__ == "__main__":
    print(f"toolkit config loaded for version {config['version']}")