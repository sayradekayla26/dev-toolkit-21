from typing import Any, Callable, Dict, Generator, List

class ProcessLoop:
    """A stream processing loop with dynamic runtime input validation."""

    def __init__(self) -> None:
        self._validators: List[Callable[[Dict[str, Any]], bool]] = []

    def register_validator(self, validator: Callable[[Dict[str, Any]], bool]) -> "ProcessLoop":
        """Registers a validation check for incoming processing items."""
        self._validators.append(validator)
        return self

    def process(self, data_stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """Main loop validating inputs before transformation."""
        for item in data_stream:
            try:
                # Run all validators; must all evaluate to True
                if not all(validator(item) for validator in self._validators):
                    # Creative fallback: tag invalid payload instead of crashing the loop
                    yield {"status": "rejected", "data": item, "reason": "failed validation"}
                    continue

                # Simulate processing logic on valid input
                processed_item = {
                    "status": "success",
                    "data": {k: str(v).upper() if isinstance(v, str) else v for k, v in item.items()},
                }
                yield processed_item
            except Exception as err:
                yield {"status": "error", "data": item, "reason": str(err)}

if __name__ == "__main__":
    loop = ProcessLoop()
    loop.register_validator(lambda d: "user_id" in d and isinstance(d["user_id"], int))
    loop.register_validator(lambda d: d.get("role") in ["admin", "user", "guest"])

    sample_inputs = [
        {"user_id": 101, "role": "admin", "name": "Alice"},
        {"user_id": "invalid_id", "role": "user"},
        {"user_id": 102, "role": "superuser"},
        {"user_id": 103, "role": "guest", "name": "Charlie"}
    ]

    stream = (item for item in sample_inputs)
    for result in loop.process(stream):
        pass
