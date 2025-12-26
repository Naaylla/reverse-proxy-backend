"""Core application components."""
from app.core.config import settings, get_settings
from app.core.logging import logger
from app.core.middleware import setup_cors

__all__ = ["settings", "get_settings", "logger", "setup_cors"]
