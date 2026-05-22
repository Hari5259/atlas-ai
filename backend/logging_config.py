"""
Logging configuration for Atlas AI
"""

import logging
import datetime
from pathlib import Path

# Create logs directory
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger("atlas_ai")
logger.setLevel(logging.DEBUG)

# Create file handler
log_file = log_dir / f"atlas_{datetime.date.today()}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Log levels for different components
def get_logger(name: str) -> logging.Logger:
    """Get logger for specific component"""
    return logging.getLogger(f"atlas_ai.{name}")

# Example loggers
conv_logger = get_logger("conversational")
api_logger = get_logger("api")
kb_logger = get_logger("knowledge_base")
