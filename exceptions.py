from typing import Optional, Any

class ToolkitError(Exception):
    """Base exception for the dev-toolkit-21 suite."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: dict[str, Any] = context or {}

class ConfigurationError(ToolkitError):
    """Raised when the runtime environment is misconfigured."""
    pass

class ProcessingError(ToolkitError):
    """Raised when data transformation fails unpredictably."""
    pass

class ValidationError(ToolkitError):
    """Raised when input data violates schema constraints."""
    def __repr__(self) -> str:
        return f"ValidationError(msg='{self}', ctx={self.context})"

def raise_if_none(value: Any, error_type: type[ToolkitError], msg: str) -> None:
    """Helper to enforce non-null values with custom exceptions."""
    if value is None:
        raise error_type(msg, {"timestamp": "now"})