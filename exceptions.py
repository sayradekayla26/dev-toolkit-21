from typing import Optional, Any

class ToolkitError(Exception):
    """Base exception for dev-toolkit-21 operations."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class ConfigurationError(ToolkitError):
    """Raised when config validation fails unexpectedly."""
    pass

class ProcessingError(ToolkitError):
    """Custom error for data pipeline failures."""
    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | context: {self.context}"

def raise_if_none(value: Any, name: str) -> None:
    """Enforce strict non-null values for internal state."""
    if value is None:
        raise ToolkitError(f"State component '{name}' cannot be null")

class RegistryViolation(ToolkitError):
    """Violation in the global toolkit component registry."""
    def __init__(self, component_id: str) -> None:
        super().__init__(f"Duplicate or invalid component: {component_id}")