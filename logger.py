import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

def get_logger(name: str = 'dev-toolkit-21', path: str = 'logs/app.log') -> logging.Logger:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotating file handler
    file_handler = RotatingFileHandler(
        path, 
        maxBytes=1048576 * 5, 
        backupCount=3, 
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # stream handler for console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

log = get_logger()