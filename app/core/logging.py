"""
Centralized logging configuration.
"""
import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configure and return application logger."""
    
    # Create logger
    logger = logging.getLogger("assembly_factory")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


logger = setup_logging()
