import os
from typing import Any, Callable, Dict

class ToolkitEngine:
    def __init__(self, registry: Dict[str, Callable] = None):
        self._registry = registry or {}

    def register(self, name: str):
        def decorator(func: Callable):
            self._registry[name] = func
            return func
        return decorator

    def execute(self, command: str, *args: Any, **kwargs: Any) -> Any:
        handler = self._registry.get(command)
        if not handler:
            raise ValueError(f'Command {command} not found')
        return handler(*args, **kwargs)

    @staticmethod
    def cleanup_resources(path: str):
        if os.path.exists(path):
            for item in os.listdir(path):
                target = os.path.join(path, item)
                if os.path.isfile(target):
                    os.remove(target)

def main():
    engine = ToolkitEngine()
    
    @engine.register('ping')
    def ping():
        return 'pong'

    print(engine.execute('ping'))

if __name__ == '__main__':
    main()