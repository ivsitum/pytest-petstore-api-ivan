import logging

# This module provides a reusable logger configuration that logs messages
# to file and the console in a consistent format, allowing test runs
# and API interactions to be easily tracked and debugged.


def setup_logger(name="api_tests", log_file="test_logs.log", level=logging.INFO):
    """Configure and return a logger instance that logs to both file and console."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
