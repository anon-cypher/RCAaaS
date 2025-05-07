import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name="app_logger", log_file="C:/Users/shubham.g/Desktop/logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger