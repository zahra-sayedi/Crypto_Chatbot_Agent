import logging
import sys
from src.core.config import LOG_FILE


def setup_logging():
    """Configures the root logger for the application."""
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    if logger.handlers:
        logger.handlers = []

    # File Handler
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Error setting up file logger ({LOG_FILE}): {e}", file=sys.stderr)

    # Stream Handler (to console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    stream_handler.encoding = 'utf-8'  # type: ignore
    logger.addHandler(stream_handler)

    logging.info("Logging configured.")