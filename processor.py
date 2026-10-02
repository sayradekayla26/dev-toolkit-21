import logging
import functools

class ResilienceEngine:
    def __init__(self, retries=3):
        self.retries = retries

    def resilient_op(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, ZeroDivisionError) as e:
                    attempts += 1
                    logging.warning(f"Attempt {attempts} failed: {e}")
                    if attempts >= self.retries:
                        return None
            return None
        return wrapper

engine = ResilienceEngine()

@engine.resilient_op
def process_data(val):
    if val < 0:
        raise ValueError("Negative value forbidden")
    return 100 / val

def batch_run(items):
    results = []
    for item in items:
        out = process_data(item)
        if out is not None:
            results.append(out)
        else:
            results.append("fallback_default")
    return results