import functools
import logging
from typing import Callable, Any

class ResilienceError(Exception):
    pass

def robust_execution(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError) as e:
                logging.error(f'Critical type mismatch: {e}')
                return None
            except Exception as e:
                attempts += 1
                if attempts >= 3:
                    raise ResilienceError(f'Failed after 3 attempts: {e}')
    return wrapper

class DataProcessor:
    def __init__(self, multiplier: int):
        self.multiplier = multiplier

    @robust_execution
    def process(self, value: Any) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError('Input must be numeric')
        if value < 0:
            raise ResilienceError('Negative input prohibited')
        return float(value * self.multiplier)

if __name__ == '__main__':
    proc = DataProcessor(2)
    print(proc.process(10))
    print(proc.process('invalid'))