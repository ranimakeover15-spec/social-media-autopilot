"""
Structured and robust logging utility for the 24/7 Autopilot pipeline.
Supports rich console output, UTF-8 safety across all OS platforms, and persistent file logging.
"""

import os
import sys
import logging
from datetime import datetime

# Enforce UTF-8 encoding on standard streams to prevent Windows console cp1252 codec errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def setup_logger(name: str = "AutopilotPipeline", log_file: str = "logs/pipeline.log") -> logging.Logger:
    """Configures and returns a logger instance with dual console and file handlers."""
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Console Formatter
    console_format = logging.Formatter(
        "\033[90m%(asctime)s\033[0m | %(levelname)-8s | \033[36m%(name)s\033[0m: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Formatter
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(console_format)
    logger.addHandler(ch)

    # File Handler
    try:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(file_format)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Warning: Could not create file logger at {log_file}: {e}")

    return logger

# Default logger instance
logger = setup_logger()
