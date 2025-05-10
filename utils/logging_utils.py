# utils/logging_utils.py

import json
import logging

# import os # Used in commented out trace section

# Configure basic structured logging


def configure_logging():
    """Configures structured logging for the application."""
    # Use standard Python logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler()

        # Cloud Logging expects logs in JSON format on stdout/stderr
        # We'll format logs as JSON strings
        formatter = CloudLoggingFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Optional: Configure logging for specific libraries if needed
    # logging.getLogger("google.cloud").setLevel(logging.WARNING)


class CloudLoggingFormatter(logging.Formatter):
    """A custom formatter to output logs in a structured JSON format for
    Cloud Logging."""

    def format(self, record):
        """Formats a log record as a JSON string."""
        # Basic structure for Cloud Logging
        log_entry = {
            "message": record.getMessage(),
            "severity": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "sourceLocation": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
            # Add other relevant fields from the log record if needed
            # e.g., trace, span_id, labels, insertId
        }

        # Add trace and span_id if available (will be integrated in Beta phase)
        # trace_id = getattr(record, 'trace_id', None)
        # span_id = getattr(record, 'span_id', None)
        # if trace_id:
        #     log_entry['logging.googleapis.com/trace'] = (
        #         f"projects/{os.getenv('GCP_PROJECT_ID')}/traces/{trace_id}"
        #     )
        # if span_id:
        #     log_entry['logging.googleapis.com/spanId'] = span_id

        # Add any extra attributes attached to the log record
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in [
                    "name",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "lineno",
                    "funcName",
                    "created",
                    "asctime",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "process",
                    "processName",
                    "message",
                    "args",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                    "severity",
                    "timestamp",
                    "sourceLocation",
                ]:  # Exclude standard attributes
                    log_entry[key] = value

        return json.dumps(log_entry)


# Example usage (for testing)


if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("An exception occurred.")
