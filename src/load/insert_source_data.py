"""
Module: insert_source_data
==========================

Loads extracted rows into PostgreSQL using the parameterised INSERT scripts
listed in ``mapping_destination.json``, then verifies the result.

Fixes over the previous version:

- ``success`` was set to ``True`` after every insert *regardless of the
  result*, so failed loads (constraint violations, type errors, missing
  connection) were logged as successes and the pipeline reported completion.
  The result of each insert is now checked and the load stops on failure.
- Rows are looked up by ``table_id`` (see ``extract.get_source_data``)
  instead of by list position.
- Each table is loaded in a single transaction: a failure part-way through
  rolls the whole table back instead of leaving it half-populated.
- Tables with no source rows are skipped instead of executing an INSERT with
  no parameters.
- Row shape is checked against the INSERT placeholder count before sending
  anything to the database, giving a clear error instead of a driver error.

New: :func:`verify_row_counts` reconciles source and destination row counts.
"""

from __future__ import annotations

import re
from typing import Dict, List

from psycopg2 import sql

import config
import db.postgresql as pgdb
import db.postgresql_queries as q
import utils.file_handler as fh
from utils.logging_handler import logger as log

DESTINATION_PATH = config.DESTINATION_PATH
_INSERT_TABLE_RE = re.compile(r"INSERT\s+INTO\s+([\w.\"]+)", re.I)


def _sorted_tables(file) -> list:
    success, queries = fh.read_json_file("Mapping Destination", file)
    if not success:
        return []
    try:
        return sorted(queries, key=lambda entry: int(entry["table_id"]))
    except (KeyError, TypeError, ValueError) as error:
        log.error(f"🔴 FAILED: invalid table_id in destination mapping: {error}")
        return []


def insert_pg_tables(database: str, file, data: Dict[int, List[tuple]]) -> bool:
    """Insert ``data`` ({table_id: rows}) into ``database``. True if all succeed."""
    tables = _sorted_tables(file)
    if not tables:
        return False

    for table in tables:
        table_id = int(table["table_id"])
        script = table["destination_query_insert"]

        if table_id not in data:
            log.error(f"🔴 FAILED: no extracted data for table_id {table_id} ({script}).")
            return False

        rows = data[table_id]
        if not rows:
            log.warning(f"🟡 SKIPPED: {script} — source returned 0 rows.")
            continue

        ok, query = fh.read_query_from_file(DESTINATION_PATH / script)
        if not ok:
            log.error(f"🔴 FAILED: {script} is missing or empty.")
            return False

        expected = query.count("%s")
        if len(rows[0]) != expected:
            log.error(
                f"🔴 FAILED: {script} expects {expected} values per row but the "
                f"source query returned {len(rows[0])} columns."
            )
            return False

        conn = pgdb.set_pg_connection(database)
        if conn is None:
            return False
        conn.autocommit = False  # one transaction per table

        if not q.pg_query(conn, database=database, query=query, values=rows):
            log.error(f"🔴 FAILED: {script} not executed; table rolled back.")
            return False

        log.info(f"🟢 SUCCESS: {script} executed ({len(rows):,} rows).")

    return True


def verify_row_counts(database: str, file, data: Dict[int, List[tuple]]) -> bool:
    """
    Compare the number of extracted rows with ``SELECT count(*)`` on each
    destination table and log a reconciliation summary.
    """
    tables = _sorted_tables(file)
    if not tables:
        return False

    all_match = True
    total_source = total_dest = 0

    for table in tables:
        table_id = int(table["table_id"])
        script = table["destination_query_insert"]
        ok, query = fh.read_query_from_file(DESTINATION_PATH / script)
        match = _INSERT_TABLE_RE.search(query) if ok else None
        if not match:
            log.error(f"🔴 FAILED: cannot determine target table from {script}.")
            all_match = False
            continue

        parts = match.group(1).replace('"', "").split(".")
        count_query = sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(*parts))
        expected = len(data.get(table_id, []))
        actual = q.pg_scalar(database, count_query)

        total_source += expected
        total_dest += actual or 0
        name = ".".join(parts)
        if actual == expected:
            log.info(f"🟢 VERIFIED: {name}: {actual:,} rows")
        else:
            all_match = False
            log.error(f"🔴 MISMATCH: {name}: source {expected:,} rows, destination {actual} rows")

    status = "🟢" if all_match else "🔴"
    log.info(f"{status} ROW COUNTS ({database}): source {total_source:,} / destination {total_dest:,}")
    return all_match
