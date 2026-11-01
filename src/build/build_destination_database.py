"""
Module: build_destination_database
==================================

Creates and drops the destination PostgreSQL objects — databases, the ETL
role, schemas, tables and permissions — from the SQL scripts in
``sql/destination``.

Fixes over the previous version:

- Every function now returns a bool on *every* path (several returned
  ``None`` from their ``except`` blocks or fell off the end).
- ``create_pg_tables`` returned the result of the *last* table only, so a
  failed CREATE for any earlier table went unnoticed. It now stops and
  reports the first failure. It also crashed with ``IndexError`` when the
  mapping had fewer than two entries (``if queries[1]:``).
- ``create_pg_role`` silently skipped (and reported failure) for any
  database whose name merely *contained* ``_test``.
- Paths use :mod:`pathlib` instead of Windows-only ``\\\\`` separators.
"""

from __future__ import annotations

import config
import db.postgresql as db
import db.postgresql_queries as q
import utils.file_handler as fh
from utils.logging_handler import logger as log

DESTINATION_PATH = config.DESTINATION_PATH


def _run_script(script: str, database: str, use_default: bool) -> bool:
    success = q.pg_query_from_file(
        path=DESTINATION_PATH / script, database=database, use_default=use_default
    )
    if success:
        log.info(f"🟢 SUCCESS: {script} executed.")
    else:
        log.error(f"🔴 FAILED: {script} not executed.")
    return success


def drop_pg_database(database: str) -> bool:
    """DROP DATABASE IF EXISTS ``database`` (connects to the admin database)."""
    return _run_script("db_database__DROP.sql", database, use_default=True)


def drop_pg_role(database: str, use_default: bool = True) -> bool:
    """DROP ROLE IF EXISTS for the ETL role (``DB_ROLE``)."""
    return _run_script("db_role__DROP.sql", database, use_default=use_default)


def create_pg_database(database: str) -> bool:
    """CREATE DATABASE ``database`` (connects to the admin database)."""
    return _run_script("db_database__CREATE.sql", database, use_default=True)


def create_pg_role(database: str) -> bool:
    """CREATE ROLE for the ETL role (``DB_ROLE``) with ``DB_ROLE_PASSWORD``."""
    return _run_script("db_role__CREATE.sql", database, use_default=True)


def grant_pg_database_permissions(database: str) -> bool:
    """Grant the ETL role CONNECT on ``database``."""
    return _run_script("db_database__GRANT.sql", database, use_default=True)


def create_pg_database_schemas(database: str) -> bool:
    """Create the destination schemas inside ``database``."""
    return _run_script("db_schemas__CREATE.sql", database, use_default=False)


def grant_pg_table_permissions(database: str) -> bool:
    """Grant the ETL role access to the schemas and tables in ``database``."""
    return _run_script("db_role__GRANT.sql", database, use_default=False)


def create_pg_tables(database: str, file) -> bool:
    """
    Run every CREATE script listed in the destination mapping file, in file
    order (execution_order, table_id). Stops at the first failure.
    """
    success, queries = fh.read_json_file("Destination Mapping", file)
    if not success:
        return False

    for table in queries:
        script = table["destination_query_create"]
        ok, query = fh.read_query_from_file(DESTINATION_PATH / script)
        if not ok:
            log.error(f"🔴 ERROR: {script} is missing or empty.")
            return False

        conn = db.set_pg_connection(database, use_default=False)
        if not q.pg_query(conn, database, query):
            log.error(f"🔴 FAILED: {script} not executed.")
            return False

        log.info(f"🟢 SUCCESS: {script} executed.")

    return True
