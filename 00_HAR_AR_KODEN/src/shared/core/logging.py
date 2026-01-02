import logging
import structlog
import sys
from .config import settings

def configure_logging():
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.ENVIRONMENT == "local":
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to intercept and redirect to structlog
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

logger = structlog.get_logger()
