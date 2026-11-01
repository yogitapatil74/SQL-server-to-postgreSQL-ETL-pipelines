"""
Module: postgresql
==================

Creates PostgreSQL connections from environment configuration.

Environment Variables
---------------------
- POSTGRESQL_HOSTNAME (default: localhost)
- POSTGRESQL_PORT (default: 5432)
- POSTGRES_DB_NAME: administrative database used for CREATE/DROP DATABASE
  (default: postgres)
- POSTGRES_DB_USERNAME (required)
- POSTGRES_DB_PASSWORD
- POSTGRESQL_CONNECT_TIMEOUT: seconds (default: 10)
"""

from __future__ import annotations

from psycopg2 import OperationalError, connect

import config
from utils.logging_handler import logger as log


def set_pg_connection(database: str | None, use_default: bool = False):
    """
    Open a connection to ``database`` (or to the administrative database when
    ``use_default`` is True). Returns ``None`` on failure.

    The connection is opened in autocommit mode, which CREATE/DROP DATABASE
    require. Callers that want a single transaction (e.g. a table load) can
    set ``conn.autocommit = False``.
    """
    db_name = config.get("POSTGRES_DB_NAME", "postgres") if use_default else database

    try:
        conn = connect(
            host=config.get("POSTGRESQL_HOSTNAME", "localhost"),
            port=config.get("POSTGRESQL_PORT", "5432"),
            dbname=db_name,
            user=config.require("POSTGRES_DB_USERNAME"),
            password=config.get("POSTGRES_DB_PASSWORD", ""),
            connect_timeout=int(config.get("POSTGRESQL_CONNECT_TIMEOUT", "10")),
        )
    except config.ConfigError as error:
        log.error(f"🔴 ERROR: {error}")
        return None
    except OperationalError as error:
        log.error(f"🔴 ERROR: could not connect to PostgreSQL database '{db_name}': {error}")
        message = str(error).lower()
        if "password authentication failed" in message:
            log.error("Check POSTGRES_DB_USERNAME / POSTGRES_DB_PASSWORD.")
        elif "connection refused" in message or "could not connect" in message:
            log.error("Ensure the PostgreSQL server is running and reachable.")
        return None

    conn.autocommit = True
    return conn
