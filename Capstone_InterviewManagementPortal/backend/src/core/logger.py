"""
Centralized application logging configuration using the standard logging module.
"""
import logging
import sys

# Configure standard stream output layout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a logger instance bound to the specific calling module path.
    """
    return logging.getLogger(module_name)