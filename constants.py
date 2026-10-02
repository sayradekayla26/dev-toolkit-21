import os
from typing import Any, Dict, Final

class ConstantVault:
    """A dynamically evaluated, environment-aware immutable constant registry.

    Provides typed access to default values, allowing overrides via environment
    variables while guaranteeing absolute immutability once loaded.
    """

    _lock: Final[set[str]] = set()
    _values: Final[Dict[str, Any]] = {}

    def __getattr__(self, name: str) -> Any:
        """Retrieves a constant, checking environment overrides first.

        Args:
            name: The name of the constant to retrieve.

        Returns:
            Any: The constant value, typed appropriately.
        """
        if name not in self._values:
            raise AttributeError(f"Constant '{name}' is not defined in the vault.")
        env_val = os.getenv(f"DEV_TOOLKIT_{name}")
        if env_val is not None:
            default_type = type(self._values[name])
            try:
                return default_type(env_val)
            except (ValueError, TypeError):
                return env_val
        return self._values[name]

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevents run-time mutation of existing constants."""
        if name in self._lock or name in ("_lock", "_values"):
            raise AttributeError("Attempting to mutate a sealed ConstantVault.")
        self._values[name] = value
        self._lock.add(name)

env: Final[ConstantVault] = ConstantVault()
env.DEFAULT_TIMEOUT = 15.0
env.MAX_WORKERS = 4
env.APP_STAGE = "development"
