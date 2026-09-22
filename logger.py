import sys
import datetime
from typing import Any

class DevLogger:
    """A creatively simple logger that prints colored status tags."""
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'END': '\033[0m'}

    def __init__(self, name: str = "dev-toolkit-21"):
        self.name = name

    def _log(self, level: str, message: Any) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        color = self.COLORS.get(level, self.COLORS['END'])
        print(f"{color}[{level}]\033[0m {timestamp} | {self.name}: {message}", file=sys.stderr)

    def info(self, msg: Any) -> None: self._log('INFO', msg)
    def warn(self, msg: Any) -> None: self._log('WARN', msg)
    def error(self, msg: Any) -> None: self._log('ERROR', msg)
    def debug(self, msg: Any) -> None: self._log('DEBUG', msg)

    def capture(self, func):
        """Decorator for wrapping functions with auto-logging."""
        def wrapper(*args, **kwargs):
            try:
                self.debug(f"calling {func.__name__}")
                return func(*args, **kwargs)
            except Exception as e:
                self.error(f"failed {func.__name__}: {str(e)}")
                raise
        return wrapper

logger = DevLogger()