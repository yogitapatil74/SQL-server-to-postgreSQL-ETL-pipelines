"""
Module: get_source_data
=======================

Runs every source SELECT script listed in ``mapping_source.json`` against SQL
Server and returns the rows **keyed by table_id**.

Why a dict instead of a list: the previous version appended each table's
rows to a list (skipping tables whose query returned no rows) and the loader
then fetched them with ``data[table_id - 1]``. A single empty source table —
or any gap in the table_id sequence — shifted every later result by one, so
rows were inserted into the *wrong destination tables* (or the load crashed
with an IndexError). Keying by table_id makes that misalignment impossible.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import config
import db.sql_server as sqldb
import utils.file_handler as fh
from utils.logging_handler import logger as log

SOURCE_PATH = config.SOURCE_PATH


def get_source_data(file=None) -> Tuple[bool, Dict[int, List[tuple]]]:
    """
    Extract source data for every table in the source mapping file.

    Returns ``(success, {table_id: rows})``. Extraction stops at the first
    missing script or failed query. A query that returns zero rows is logged
    as a warning and kept as an empty list.
    """
    success, queries = fh.read_json_file("Mapping Source", file or config.SOURCE_MAPPING_FILE)
    if not success:
        return False, {}

    try:
        queries = sorted(queries, key=lambda entry: int(entry["table_id"]))
    except (KeyError, TypeError, ValueError) as error:
        log.error(f"🔴 FAILED: invalid table_id in source mapping: {error}")
        return False, {}

    conn = sqldb.connect_sql_server()
    if conn is None:
        return False, {}

    data: Dict[int, List[tuple]] = {}
    try:
        for table in queries:
            table_id = int(table["table_id"])
            script = table["source_query_select"]

            ok, query = fh.read_query_from_file(SOURCE_PATH / script)
            if not ok:
                log.error(f"🔴 FAILED: {script} does not contain a query.")
                return False, {}

            ok, rows = sqldb.execute_sql_query(conn, query)
            if not ok:
                log.error(f"🔴 FAILED: {script} not executed.")
                return False, {}

            if rows:
                log.info(f"🟢 SUCCESS: {script} executed ({len(rows):,} rows).")
            else:
                log.warning(f"🟡 WARNING: {script} returned 0 rows.")
            data[table_id] = rows

        return True, data

    finally:
        conn.close()
