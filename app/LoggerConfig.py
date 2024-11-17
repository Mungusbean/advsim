import logging

def setup_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    class CustomFormatter(logging.Formatter):
        level_colors = {
            logging.DEBUG: "\033[36m",  # Cyan
            logging.INFO: "\033[32m",   # Green
            logging.WARNING: "\033[33m",  # Yellow
            logging.ERROR: "\033[31m",  # Red
            logging.CRITICAL: "\033[35;1m",  # Bright Magenta
        }
        reset = "\033[0m"  # Reset color

        def format(self, record):
            log_color = self.level_colors.get(record.levelno, self.reset)
            original_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(f"{log_color}{original_format}{self.reset}")
            return formatter.format(record)

    handler.setFormatter(CustomFormatter())

    if not logger.handlers:
        logger.addHandler(handler)

    return logger