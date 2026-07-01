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

