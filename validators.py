from typing import Any, Callable, Dict, List, Optional

class ValidationError(Exception):
    """Custom exception for dev-toolkit-21 input failures."""
    pass

def validate_payload(data: Any, schema: Dict[str, type]) -> bool:
    """Creative schema enforcement using type introspection."""
    if not isinstance(data, dict):
        raise ValidationError(f"Payload expected dict, got {type(data).__name__}")
    
    for key, expected_type in schema.items():
        val = data.get(key)
        if val is None or not isinstance(val, expected_type):
            raise ValidationError(f"Invalid field {key}: expected {expected_type.__name__}")
    return True

def main_loop_processor(data_stream: List[Dict[str, Any]]):
    """Processing loop with robust input validation."""
    schema = {"id": int, "payload": str}
    
    for entry in data_stream:
        try:
            if validate_payload(entry, schema):
                process_data(entry)
        except ValidationError as e:
            print(f"Skipping malformed entry: {e}")
            continue

def process_data(item: Dict[str, Any]):
    """Simulated core processing logic."""
    print(f"Processing secure item {item['id']}: {item['payload'][:10]}...")

if __name__ == '__main__':
    mock_data = [{"id": 1, "payload": "data_alpha"}, {"invalid": True}]
    main_loop_processor(mock_data)