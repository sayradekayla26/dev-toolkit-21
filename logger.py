import sys
import time
import inspect
from typing import Any

class DataLogger:
    def __init__(self, stream=sys.stdout, prefix='[DEV-TOOLKIT-21]'):
        self.stream = stream
        self.prefix = prefix
        self.history = []

    def __call__(self, data: Any, level: str = 'INFO') -> None:
        frame = inspect.stack()[1]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        caller = f"{frame.function}:{frame.lineno}"
        
        payload = {
            "ts": timestamp,
            "lvl": level.upper(),
            "src": caller,
            "val": str(data)
        }
        
        self.history.append(payload)
        formatted = f"{self.prefix} {payload['ts']} | {payload['lvl']} | {payload['src']} >> {payload['val']}"
        self.stream.write(formatted + '\n')
        self.stream.flush()

    def dump_session(self) -> list:
        return self.history

    def clear(self) -> None:
        self.history.clear()

logger = DataLogger()