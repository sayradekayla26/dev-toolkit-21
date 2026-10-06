from typing import Any, Callable, Dict, Optional

class DataGuard:
    def __init__(self):
        self._registry: Dict[str, Callable[[Any], bool]] = {}

    def register(self, key: str, validator: Callable[[Any], bool]):
        self._registry[key] = validator

    def validate(self, schema: Dict[str, str], payload: Dict[str, Any]) -> bool:
        try:
            return all(self._registry[rule](payload.get(field)) for field, rule in schema.items())
        except (KeyError, TypeError):
            return False

def is_non_empty_str(val: Any) -> bool:
    return isinstance(val, str) and len(val.strip()) > 0

def is_positive_int(val: Any) -> bool:
    return isinstance(val, int) and val > 0

# Main loop integration example
class InputProcessor:
    def __init__(self):
        self.guard = DataGuard()
        self.guard.register('string', is_non_empty_str)
        self.guard.register('positive', is_positive_int)

    def process_loop(self, stream: list):
        schema = {'name': 'string', 'age': 'positive'}
        for item in stream:
            if not isinstance(item, dict) or not self.guard.validate(schema, item):
                print(f"Discarding invalid input: {item}")
                continue
            self.execute_task(item)

    def execute_task(self, data: Dict[str, Any]):
        print(f"Processing: {data['name']}")