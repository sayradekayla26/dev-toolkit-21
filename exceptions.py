import sys
import traceback
from typing import Any, Dict, Optional, Type


class ErrorRegistryMeta(type):
    """Metaclass that automatically registers toolkit exceptions for dynamic lookup."""
    _registry: Dict[str, Type["ToolkitError"]] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "ToolkitError" and issubclass(cls, Exception):
            mcs._registry[name] = cls
        return cls

    @classmethod
    def get_registered(mcs) -> Dict[str, Type["ToolkitError"]]:
        return dict(mcs._registry)


class ToolkitError(Exception, metaclass=ErrorRegistryMeta):
    """Base exception supporting contextual payloads and origin frame capture."""

    def __init__(self, message: str, *, code: int = 500, **context: Any):
        super().__init__(message)
        self.message = message
        self.code = code
        self.context = context
        self.origin = self._capture_origin()

    def _capture_origin(self) -> str:
        stack = traceback.extract_stack(limit=3)
        if len(stack) >= 2:
            frame = stack[-2]
            return f"{frame.filename}:{frame.lineno} in {frame.name}"
        return "unknown"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "origin": self.origin,
            "context": self.context,
        }

    @classmethod
    def wrap(cls, exc: Exception, default_msg: Optional[str] = None) -> "ToolkitError":
        msg = default_msg or str(exc) or exc.__class__.__name__
        instance = cls(msg, original_exception=exc.__class__.__name__)
        instance.__cause__ = exc
        return instance


class ConfigurationError(ToolkitError):
    """Raised when configuration validation or parsing fails."""


class ProcessingPipelineError(ToolkitError):
    """Raised during data transformation or workflow processing errors."""


class ValidationFailedError(ToolkitError):
    """Raised when runtime validation or assertion checks fail."""
