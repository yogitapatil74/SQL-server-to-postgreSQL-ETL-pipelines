"""
Module: file_handler
====================

Helpers for reading the JSON mapping files and SQL script files used by the
pipeline.

Every function returns a ``(success, value)`` tuple in *all* cases. The
previous version returned ``None`` from its ``except`` blocks, so callers that
unpacked ``success, data = ...`` crashed with ``TypeError: cannot unpack
non-iterable NoneType`` instead of logging a clean failure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import utils.validation_handler as vh
from utils.logging_handler import logger as log


def read_json_file(name: str, file: str | Path) -> Tuple[bool, list]:
    """Load a JSON file and check that it holds a non-empty list."""
    success, queries = load_json_file(file)

    if success:
        log.info(f"🟢 SUCCESS: {name} JSON file read.")
    else:
        log.error(f"🔴 FAILED: {name} JSON file was not read.")
        return False, []

    if not isinstance(queries, list) or not vh.validate_list(f"{name} JSON File", queries):
        log.error(f"🔴 FAILED: {name} JSON file does not contain a list of entries.")
        return False, []

    return True, queries


def load_json_file(file: str | Path) -> Tuple[bool, list]:
    """Read raw JSON content from ``file``."""
    try:
        with open(file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        log.error(f"🔴 ERROR: JSON file not found: {file}")
        return False, []
    except json.JSONDecodeError as error:
        log.error(f"🔴 ERROR: Invalid JSON in {file}: {error}")
        return False, []

    if not data:
        log.error(f"🔴 ERROR: JSON file is empty: {file}")
        return False, []

    return True, data


def read_query_from_file(path: str | Path) -> Tuple[bool, str]:
    """
    Read a SQL script and normalise its whitespace.

    Newlines and tabs are replaced with spaces. The previous version deleted
    them outright, which silently glued tokens together whenever a line did
    not end or begin with whitespace (e.g. ``SELECT a\\nFROM t`` became
    ``SELECT aFROM t``). A UTF-8 byte-order mark, which SQL Server Management
    Studio adds to saved scripts, is also stripped.
    """
    try:
        with open(path, "r", encoding="utf-8-sig") as handle:
            query = handle.read()
    except FileNotFoundError:
        log.error(f"🔴 ERROR: SQL file not found: {path}")
        return False, ""
    except OSError as error:
        log.error(f"🔴 ERROR: Could not read {path}: {error}")
        return False, ""

    query = query.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip()
    return bool(query), query


def get_query_list_from_file(name: str, queries: list) -> Tuple[bool, list]:
    """Return ``[(table_id, query[name]), ...]`` for a list of mapping entries."""
    try:
        query_list = [(int(query["table_id"]), query[name]) for query in queries]
    except (KeyError, TypeError, ValueError) as error:
        log.error(f"🔴 FAILED: could not build '{name}' query list: {error}")
        return False, []

    return vh.validate_list(name, query_list), query_list
