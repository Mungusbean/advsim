import logging

def setup_logger(name=None):
    # Create a logger with the given name (or root if none)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the minimum log level

    # Create console handler and set level to debug
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:  # Avoid adding multiple handlers if imported in multiple places
        logger.addHandler(handler)
    
    return logger

