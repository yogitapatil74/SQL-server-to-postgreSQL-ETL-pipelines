"""
Module: sql_server
==================

Executes SELECT queries against SQL Server through pyodbc.

Environment Variables
---------------------
- SQLSERVER_CONN : ODBC connection string (required)
- SQLSERVER_TIMEOUT : login timeout in seconds (default: 30)

Fixes over the previous version:

- ``execute_sql_query`` returned ``None`` on errors, so the caller's
  ``success, data = ...`` raised ``TypeError``. It now always returns a tuple.
- An empty result set is no longer reported as a failure — "query ran and
  returned 0 rows" and "query failed" are different outcomes.
- A caller-supplied connection is no longer closed behind the caller's back,
  which lets one connection be reused for all source queries instead of
  opening a new one per table.
- ``pyodbc`` is imported lazily, so validation, tests and documentation
  builds do not need the ODBC driver manager installed.
"""

from __future__ import annotations

from typing import Tuple

import config
from utils.logging_handler import logger as log


def connect_sql_server():
    """Open a SQL Server connection, or return None on failure."""
    try:
        import pyodbc  # noqa: PLC0415  (lazy import)

        return pyodbc.connect(
            config.require("SQLSERVER_CONN"),
            timeout=int(config.get("SQLSERVER_TIMEOUT", "30")),
        )
    except config.ConfigError as error:
        log.error(f"🔴 ERROR: {error}")
    except ImportError as error:
        log.error(f"🔴 ERROR: pyodbc is not available: {error}")
    except Exception as error:  # pyodbc.Error and friends
        log.error(f"🔴 ERROR: could not connect to SQL Server: {error}")
    return None


def execute_sql_query(conn, query: str) -> Tuple[bool, list]:
    """
    Run ``query`` and return ``(success, rows)`` where each row is a tuple.

    If ``conn`` is None a temporary connection is opened and closed again;
    otherwise the caller owns (and must close) the connection.
    """
    owns_connection = conn is None
    if owns_connection:
        conn = connect_sql_server()
        if conn is None:
            return False, []

    try:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = [tuple(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
        return True, rows

    except Exception as error:  # pyodbc.Error and friends
        log.error(f"🔴 ERROR: SQL Server query failed: {error}\nQuery: {query[:500]}")
        return False, []

    finally:
        if owns_connection:
            conn.close()
