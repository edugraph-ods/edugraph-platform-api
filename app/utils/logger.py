import logging
from typing import Optional

"""
configure_logging is a function that configures the logging.

Args:
    level (str): The level of the logging.

Returns:
    None
"""
def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

"""
get_logger is a function that returns a logger.

Args:
    name (Optional[str]): The name of the logger.

Returns:
    logging.Logger: A logger.
"""
def get_logger(name: Optional[str] = None) -> logging.Logger:
    if not logging.getLogger().handlers:
        configure_logging()
    return logging.getLogger(name if name else "edugraph")
