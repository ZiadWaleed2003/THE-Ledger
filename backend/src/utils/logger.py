import logging
import os
import uuid
import datetime

# Global singleton to store the logger instance
_logger_instance = None
_session_id = None

def get_session_logger():
    global _logger_instance, _session_id

    # If logger already exists, return it
    if _logger_instance:
        return _logger_instance, _session_id
    
    # unique Id for every session 
    _session_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    
    log_dir = "backend/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # merging the 2 paths together
    log_filename = os.path.join(log_dir, f"{timestamp}_{_session_id}.log")

    logger = logging.getLogger(_session_id)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_filename)
    
    # just some normal formatting
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    _logger_instance = logger

    return _logger_instance