"""
config.py — Centralised, cross-platform configuration
=====================================================

Loads settings from environment variables (and an optional ``.env`` file in
the repository root) and exposes filesystem paths as :class:`pathlib.Path`
objects.

Previously every module built paths with hard-coded Windows separators
(``f"{SQL_PATH}\\\\destination"``), so the pipeline could not run on Linux,
macOS, Docker or CI. Paths now default to locations relative to the
repository, and any of them can still be overridden through the environment.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_PATH = Path(__file__).resolve().parent.parent

# Load <repo>/.env if present. Real environment variables take precedence.
load_dotenv(ROOT_PATH / ".env", override=False)


class ConfigError(RuntimeError):
    """Raised when a required configuration value is missing."""


def get(name: str, default: str | None = None) -> str | None:
    """Return an environment value, treating empty strings as unset."""
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value.strip()


def require(name: str) -> str:
    """Return a required environment value or raise :class:`ConfigError`."""
    value = get(name)
    if value is None:
        raise ConfigError(
            f"Missing required setting '{name}'. Add it to your .env file "
            "(see .env.example)."
        )
    return value


def _path(name: str, default: Path) -> Path:
    value = get(name)
    return Path(value).expanduser() if value else default


SQL_PATH = _path("SQL_PATH", ROOT_PATH / "sql")
SOURCE_PATH = SQL_PATH / "source"
DESTINATION_PATH = SQL_PATH / "destination"
LOGS_PATH = _path("LOGS_PATH", ROOT_PATH / "logs")

MAPPING_FILE = SQL_PATH / "mapping.csv"
SOURCE_MAPPING_FILE = SQL_PATH / "mapping_source.json"
DESTINATION_MAPPING_FILE = SQL_PATH / "mapping_destination.json"

LOG_LEVEL = (get("LOG_LEVEL", "INFO") or "INFO").upper()
DB_ROLE = get("DB_ROLE", "etl_user")

# Rows sent to PostgreSQL per execute_batch() round trip. The original value
# of 100 made loading ~485k rows needlessly slow.
INSERT_PAGE_SIZE = int(get("INSERT_PAGE_SIZE", "1000"))
