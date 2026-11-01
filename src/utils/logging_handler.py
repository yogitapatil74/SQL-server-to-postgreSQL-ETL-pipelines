"""
Module: logging_handler
=======================

Initialises application logging: a level-specific log file (``app.log`` for
INFO, ``debug.log`` for DEBUG, ``error.log`` for ERROR), console output, and
a dedicated ``error.log`` that always receives ERROR records.

Environment Variables
---------------------
- LOGS_PATH : directory for log files (default: ``<repo>/logs``)
- LOG_LEVEL : DEBUG, INFO, WARNING or ERROR (default: INFO)

Fixes over the previous version:

- Paths are built with :mod:`pathlib` (previously ``LOGS_PATH\\\\file``, which
  only worked on Windows) and the log directory is created if missing.
- An invalid or missing ``LOG_LEVEL`` falls back to INFO instead of passing
  ``None`` to the handlers.
- ``error.log`` now uses the same timestamped format as the main log file.
- Re-importing the module no longer attaches duplicate handlers.
"""

import logging

import config

_FILE_FORMAT = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_CONSOLE_FORMAT = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")

logger = logging.getLogger()

_level = getattr(logging, config.LOG_LEVEL, None)
log_level = _level if isinstance(_level, int) else logging.INFO

_LEVEL_FILES = {
    logging.DEBUG: "debug.log",
    logging.INFO: "app.log",
    logging.ERROR: "error.log",
}
log_file = _LEVEL_FILES.get(log_level, "app.log")


def _configure() -> None:
    if getattr(logger, "_etl_configured", False):
        return

    config.LOGS_PATH.mkdir(parents=True, exist_ok=True)
    logger.setLevel(log_level)

    main_handler = logging.FileHandler(config.LOGS_PATH / log_file, encoding="utf-8")
    main_handler.setLevel(log_level)
    main_handler.setFormatter(_FILE_FORMAT)
    logger.addHandler(main_handler)

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(_CONSOLE_FORMAT)
    logger.addHandler(console)

    if log_file != "error.log":
        error_handler = logging.FileHandler(
            config.LOGS_PATH / "error.log", encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(_FILE_FORMAT)
        logger.addHandler(error_handler)

    logger._etl_configured = True


_configure()
