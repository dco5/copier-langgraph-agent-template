"""
Structured logging configuration using structlog.
Provides request context binding and environment-specific formatting.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from src.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.is_production:
        # Production: JSON output for log aggregation
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Development: Colored console output
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.debug else logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.debug else logging.INFO,
    )

    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a logger instance with optional name binding."""
    logger = structlog.get_logger()
    if name:
        logger = logger.bind(logger_name=name)
    return logger


def bind_context(**kwargs: Any) -> None:
    """Bind context variables to the current logger context."""
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """Clear all context variables."""
    structlog.contextvars.clear_contextvars()


def unbind_context(*keys: str) -> None:
    """Remove specific keys from the context."""
    structlog.contextvars.unbind_contextvars(*keys)


# Pre-configured loggers for common use cases
class Loggers:
    """Pre-configured logger instances."""

    @staticmethod
    def agent() -> structlog.stdlib.BoundLogger:
        return get_logger("agent")

    @staticmethod
    def api() -> structlog.stdlib.BoundLogger:
        return get_logger("api")

    @staticmethod
    def auth() -> structlog.stdlib.BoundLogger:
        return get_logger("auth")

    @staticmethod
    def database() -> structlog.stdlib.BoundLogger:
        return get_logger("database")

    @staticmethod
    def llm() -> structlog.stdlib.BoundLogger:
        return get_logger("llm")

    @staticmethod
    def memory() -> structlog.stdlib.BoundLogger:
        return get_logger("memory")

    @staticmethod
    def tools() -> structlog.stdlib.BoundLogger:
        return get_logger("tools")
