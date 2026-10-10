import sys
import traceback
from typing import Any, Callable

def execute_with_resilience(func: Callable, *args, **kwargs) -> Any:
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        error_payload = {
            "error_type": type(e).__name__,
            "stack_trace": traceback.format_exc(),
            "context": {"args": args, "kwargs": kwargs}
        }
        print(f"[dev-toolkit-21] recovery sequence initiated: {error_payload['error_type']}", file=sys.stderr)
        return None

def safe_wrapper(func: Callable):
    def decorator(*args, **kwargs):
        result = execute_with_resilience(func, *args, **kwargs)
        if result is None:
            return []
        return result
    return decorator

if __name__ == "__main__":
    @safe_wrapper
    def risky_operation(data):
        return [1 / int(i) for i in data]

    output = risky_operation(['1', '0', '2'])
    print(f"processed data: {output}")