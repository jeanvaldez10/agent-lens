import logging
import os
import sys

from agentlens.logging.formatters import agentlensLogFileFormatter, agentlensLogFormatter


class _CurrentStderrHandler(logging.StreamHandler):
    """StreamHandler that writes to whatever ``sys.stderr`` is at emit time.

    A plain ``StreamHandler`` binds the stream object at creation. If that stream is later
    replaced and closed (e.g. by pytest's output capture, or during interpreter shutdown),
    every subsequent log call - including ones from ``atexit`` hooks and ``__del__`` -
    fails with "I/O operation on closed file". Mirrors ``logging.lastResort``.
    """

    @property
    def stream(self):
        return sys.stderr

    @stream.setter
    def stream(self, value):
        # The stream is always resolved dynamically; ignore assignments from the base class.
        pass


# Create the logger at module level
logger = logging.getLogger("agentlens")
logger.propagate = False
logger.setLevel(logging.CRITICAL)


def configure_logging(config=None):  # Remove type hint temporarily to avoid circular import
    """Configure the agentlens logger with console and optional file handlers.

    Args:
        config: Optional Config instance. If not provided, a new Config instance will be created.
    """
    # Defer the Config import to avoid circular dependency
    if config is None:
        from agentlens.config import Config

        config = Config()

    # Use env var as override if present, otherwise use config
    log_level_env = os.environ.get("AGENTLENS_LOG_LEVEL", "").upper()
    if log_level_env and hasattr(logging, log_level_env):
        log_level = getattr(logging, log_level_env)
    else:
        # Handle string log levels from config
        if isinstance(config.log_level, str):
            log_level_str = config.log_level.upper()
            if hasattr(logging, log_level_str):
                log_level = getattr(logging, log_level_str)
            else:
                log_level = logging.INFO
        else:
            log_level = config.log_level if isinstance(config.log_level, int) else logging.INFO

    logger.setLevel(log_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    # Configure console logging
    stream_handler = _CurrentStderrHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(agentlensLogFormatter())
    logger.addHandler(stream_handler)

    # Configure file logging if enabled
    log_to_file = os.environ.get("AGENTLENS_LOGGING_TO_FILE", "True").lower() == "true"
    if log_to_file:
        file_handler = logging.FileHandler("agentlens.log", mode="w")
        file_handler.setLevel(log_level)
        formatter = agentlensLogFileFormatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def intercept_opentelemetry_logging():
    """
    Configure OpenTelemetry logging to redirect all messages to the agentlens logger.
    All OpenTelemetry logs will be prefixed with [opentelemetry.X] and set to DEBUG level.
    """
    prefix = "opentelemetry"
    otel_root_logger = logging.getLogger(prefix)
    otel_root_logger.propagate = False
    otel_root_logger.setLevel(logging.DEBUG)  # capture all

    for handler in otel_root_logger.handlers[:]:
        otel_root_logger.removeHandler(handler)

    # Create a handler that forwards all messages to the agentlens logger
    class OtelLogHandler(logging.Handler):
        def emit(self, record):
            if record.name.startswith(f"{prefix}."):
                module_name = record.name.replace(f"{prefix}.", "", 1)
            else:
                module_name = record.name
            message = f"[{prefix}.{module_name}] {record.getMessage()}"
            logger.debug(message)

    otel_root_logger.addHandler(OtelLogHandler())
