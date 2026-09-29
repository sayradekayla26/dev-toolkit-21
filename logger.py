import logging
import functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev-toolkit-21')

def validate_inputs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg is None for arg in args):
            logger.error('invalid input detected: null argument found')
            return None
        return func(*args, **kwargs)
    return wrapper

class DataProcessor:
    def __init__(self):
        self.pipeline = []

    @validate_inputs
    def process_node(self, payload):
        if not isinstance(payload, dict):
            raise ValueError('payload must be a dictionary')
        logger.info(f'processing: {payload.keys()}')
        return True

    def run_main_loop(self, queue):
        while queue:
            item = queue.pop(0)
            try:
                status = self.process_node(item)
                if status:
                    logger.info('execution successful')
            except Exception as e:
                logger.warning(f'skipped malicious or malformed block: {e}')

if __name__ == '__main__':
    proc = DataProcessor()
    proc.run_main_loop([{'id': 1}, None, {'id': 2}])