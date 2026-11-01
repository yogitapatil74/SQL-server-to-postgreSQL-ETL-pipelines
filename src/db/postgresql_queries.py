"""
Module: postgresql_queries
==========================

Executes SQL against PostgreSQL: plain statements, parameterised batch
inserts, scripts rendered from template files, and scalar queries.

Fixes over the previous version:

- ``pg_query`` always returns a bool (it returned ``None`` on every error
  path), creates its cursor inside the ``try`` block, and handles a failed
  connection instead of crashing on ``None.cursor()``.
- Removed the mutable default argument ``values: list = []``.
- Removed dead code that substituted ``$password`` *after* the query had
  already been executed.
- Template values are validated / escaped before being substituted into SQL:
  database and role names must be plain identifiers, and the role password
  has single quotes escaped. Previously a password containing ``'`` broke the
  CREATE ROLE statement, and an arbitrary ``--database`` value was pasted
  straight into DROP/CREATE DATABASE.
"""

from __future__ import annotations

import re
from string import Template

from psycopg2 import Error
from psycopg2.extras import execute_batch

import config
import db.postgresql as db
import utils.file_handler as fh
from utils.logging_handler import logger as log

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,62}$")


def validate_identifier(name: str, kind: str = "identifier") -> str:
    """Return ``name`` if it is a safe, unquoted PostgreSQL identifier."""
    if not isinstance(name, str) or not _IDENTIFIER_RE.match(name):
        raise ValueError(
            f"Invalid {kind} '{name}': use letters, digits and underscores only, "
            "starting with a letter or underscore (max 63 characters)."
        )
    return name


def render_sql(query: str, database: str | None = None) -> str:
    """Substitute ``$database``, ``$role`` and ``$password`` placeholders."""
    values: dict[str, str] = {}
    if "$database" in query:
        values["database"] = validate_identifier(database, "database name")
    if "$role" in query:
        values["role"] = validate_identifier(config.DB_ROLE, "role name (DB_ROLE)")
    if "$password" in query:
        values["password"] = config.require("DB_ROLE_PASSWORD").replace("'", "''")
    return Template(query).safe_substitute(values) if values else query


def pg_query(conn, database: str, query: str, values: list | None = None,
             page_size: int | None = None) -> bool:
    """
    Execute ``query`` (optionally as a batch over ``values``), commit, and
    close the connection. Returns True on success, False on any failure.
    """
    if conn is None:
        conn = db.set_pg_connection(database)
    if conn is None:
        log.error(f"🔴 ERROR: no connection to '{database}'; query not executed.")
        return False

    try:
        with conn.cursor() as cursor:
            if values:
                execute_batch(cursor, query, values,
                              page_size=page_size or config.INSERT_PAGE_SIZE)
            else:
                cursor.execute(query)
        conn.commit()
        return True

    except Error as error:
        _safe_rollback(conn)
        log.error(f"🔴 ERROR: PostgreSQL error on '{database}': {error}".rstrip())
        return False

    except Exception as error:  # pylint: disable=broad-except
        _safe_rollback(conn)
        log.error(f"🔴 ERROR: {error}", exc_info=True)
        return False

    finally:
        conn.close()


def pg_query_from_file(path, database: str, use_default: bool) -> bool:
    """Read a SQL script, render its placeholders and execute it."""
    success, query = fh.read_query_from_file(path)
    if not success:
        log.error(f"🔴 ERROR: {path} is missing or empty.")
        return False

    try:
        query = render_sql(query, database)
    except (ValueError, config.ConfigError) as error:
        log.error(f"🔴 ERROR: {error}")
        return False

    conn = db.set_pg_connection(database, use_default)
    return pg_query(conn, database, query)


def pg_scalar(database: str, query, params: tuple | None = None):
    """Run a query returning a single value. Returns None on failure."""
    conn = db.set_pg_connection(database)
    if conn is None:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
        return row[0] if row else None
    except Error as error:
        log.error(f"🔴 ERROR: PostgreSQL error on '{database}': {error}".rstrip())
        return None
    finally:
        conn.close()


def _safe_rollback(conn) -> None:
    try:
        conn.rollback()
    except Exception:  # pylint: disable=broad-except
        pass
