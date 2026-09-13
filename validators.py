import functools

class ValidationError(Exception):
    """Custom exception for dev-toolkit-21 pipeline flow."""
    pass

def validate_input(func):
    """Decorates processing loop steps to verify payload integrity."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        data = kwargs.get('data') or (args[0] if args else None)
        if not isinstance(data, dict):
            raise ValidationError(f"Expected dict, received {type(data).__name__}")
        if 'uid' not in data:
            raise ValidationError("Missing required uid in payload")
        return func(*args, **kwargs)
    return wrapper

class InputProcessor:
    """Processing engine with strict validation constraints."""
    def __init__(self, registry=None):
        self.registry = registry or {}

    @validate_input
    def process_node(self, data):
        """Executes atomic logic units after validation."""
        uid = data['uid']
        self.registry[uid] = data.get('payload', 'initialized')
        return f"Processed {uid}"

def run_main_loop(items):
    """Main orchestration loop for dev-toolkit-21 tasks."""
    proc = InputProcessor()
    results = []
    for item in items:
        try:
            results.append(proc.process_node(data=item))
        except ValidationError as e:
            results.append(f"Skipping invalid entry: {e}")
    return results