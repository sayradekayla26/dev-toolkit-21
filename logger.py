import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='dev-toolkit-21', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        # Creative custom formatter using internal dict-access for performance
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Standard rotation with a byte-size limit of 5MB
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Stream to console for debugging visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

if __name__ == '__main__':
    log = setup_logger()
    log.info('toolkit initialized successfully')