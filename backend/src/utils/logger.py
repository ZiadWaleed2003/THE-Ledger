import logging
import os
import uuid
import datetime

def setup_session_logger():
    
    # unique Id for every session 
    session_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    
    log_dir = "backend/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # merging the 2 paths together
    log_filename = os.path.join(log_dir, f"{timestamp}_{session_id}.log")

    logger = logging.getLogger(session_id)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_filename)
    
    # just some normal formatting
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger, session_id