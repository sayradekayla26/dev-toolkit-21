import logging
from logging.handlers import RotatingFileHandler
import os

def get_dev_logger(name='dev-toolkit-21', log_file='app.log'):
    """
    custom rotating logger factory for dev environments
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # rotate at 5MB, keep 3 historical backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    # ensure we do not duplicate handlers if called twice
    if not logger.handlers:
        logger.addHandler(handler)
        # stream output for real-time console feedback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# global singleton for easy access across the project
app_logger = get_dev_logger()