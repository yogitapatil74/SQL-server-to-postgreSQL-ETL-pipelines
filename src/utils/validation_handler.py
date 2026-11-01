"""
Module: validation_handler
==========================

Validation utilities, including a pre-flight check of the whole mapping that
runs *before* any database is dropped.

The original pipeline dropped the destination databases first and only then
discovered missing SQL files, so a typo in ``mapping.csv`` destroyed the
existing data and left nothing in its place. :func:`validate_mapping` catches
those problems up front, without touching any database.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

from utils.logging_handler import logger as log

_CREATE_RE = re.compile(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.\"]+)", re.I)
_INSERT_RE = re.compile(r"INSERT\s+INTO\s+([\w.\"]+)\s*\(([^)]*)\)", re.I | re.S)
_REFERENCES_RE = re.compile(r"REFERENCES\s+([\w.\"]+)", re.I)
_SELECT_PREFIX_RE = re.compile(r"^\s*SELECT\s+(?:TOP\s+\(?\d+\)?\s+)?(?:DISTINCT\s+)?", re.I)
_FROM_RE = re.compile(r"\bFROM\b", re.I)


def count_select_columns(query: str) -> int | None:
    """
    Count the top-level columns of a simple ``SELECT ... FROM`` statement,
    ignoring commas inside parentheses (e.g. ``CAST(x AS DECIMAL(18,2))``).
    Returns None for statements this heuristic cannot handle.
    """
    if not _SELECT_PREFIX_RE.match(query) or not _FROM_RE.search(query):
        return None
    body = _SELECT_PREFIX_RE.sub("", _FROM_RE.split(query, maxsplit=1)[0], count=1)
    depth, count = 0, 1
    for char in body:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            count += 1
    return count


def validate_list(name: str, list_object) -> bool:
    """Return True if ``list_object`` is a non-empty list; log otherwise."""
    if isinstance(list_object, list) and list_object:
        return True
    log.error(f"🔴 ERROR: {name} is empty.")
    return False


@dataclass
class MappingReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    tables: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _table_name(raw: str) -> str:
    return raw.replace('"', "").lower()


def validate_mapping(mapping_file: Path, source_dir: Path, destination_dir: Path) -> MappingReport:
    """
    Check every application table (``is_app_table == 1``) in ``mapping.csv``.

    Errors (pipeline must not run):
      - duplicate / missing / non-integer ``table_id``
      - missing or empty SELECT, CREATE or INSERT script
      - INSERT column count different from its ``%s`` placeholder count
      - SELECT column count different from the INSERT placeholder count
      - INSERT targeting a different table than its CREATE script
      - a foreign key to a table that is not part of the migration, or that
        would be created / loaded *after* the referencing table
    Warnings:
      - ``destination_schema.destination_table`` in the CSV not matching the
        table actually created by the CREATE script
    """
    report = MappingReport()

    try:
        with open(mapping_file, newline="", encoding="utf-8-sig") as handle:
            rows = [r for r in csv.DictReader(handle) if str(r.get("is_app_table", "")).strip() == "1"]
    except FileNotFoundError:
        report.errors.append(f"Mapping file not found: {mapping_file}")
        return report

    if not rows:
        report.errors.append(f"No application tables (is_app_table = 1) in {mapping_file}")
        return report

    tables: dict[str, dict] = {}
    seen_ids: set[int] = set()

    for row in rows:
        label = row.get("source_table") or row.get("destination_table") or "?"
        try:
            table_id = int(str(row["table_id"]).strip())
            execution_order = int(str(row.get("execution_order") or 0).strip())
        except (KeyError, ValueError):
            report.errors.append(f"{label}: table_id/execution_order must be integers")
            continue
        if table_id in seen_ids:
            report.errors.append(f"{label}: duplicate table_id {table_id}")
            continue
        seen_ids.add(table_id)

        texts = {}
        for column, folder in (
            ("source_query_select", source_dir),
            ("destination_query_create", destination_dir),
            ("destination_query_insert", destination_dir),
        ):
            name = (row.get(column) or "").strip()
            path = folder / name
            if not name or not path.is_file():
                report.errors.append(f"[{table_id}] {label}: missing {column} file '{name}'")
                continue
            text = path.read_text(encoding="utf-8-sig")
            if not text.strip():
                report.errors.append(f"[{table_id}] {label}: {name} is empty")
                continue
            texts[column] = text

        create = texts.get("destination_query_create", "")
        insert = texts.get("destination_query_insert", "")

        created = _CREATE_RE.search(create)
        created_name = _table_name(created.group(1)) if created else None
        if create and not created_name:
            report.errors.append(f"[{table_id}] {label}: no CREATE TABLE statement found")

        if insert:
            match = _INSERT_RE.search(insert)
            if not match:
                report.errors.append(f"[{table_id}] {label}: no 'INSERT INTO table (columns)' found")
            else:
                insert_name = _table_name(match.group(1))
                columns = [c for c in match.group(2).split(",") if c.strip()]
                placeholders = insert.count("%s")
                if len(columns) != placeholders:
                    report.errors.append(
                        f"[{table_id}] {label}: INSERT lists {len(columns)} columns "
                        f"but has {placeholders} placeholders"
                    )
                select_columns = count_select_columns(texts.get("source_query_select", ""))
                if select_columns is not None and select_columns != placeholders:
                    report.errors.append(
                        f"[{table_id}] {label}: SELECT returns {select_columns} columns "
                        f"but INSERT expects {placeholders}"
                    )
                if created_name and insert_name != created_name:
                    report.errors.append(
                        f"[{table_id}] {label}: INSERT targets {insert_name} but CREATE builds {created_name}"
                    )

        if created_name:
            csv_name = f"{row.get('destination_schema', '')}.{row.get('destination_table', '')}".lower()
            if csv_name != created_name:
                report.warnings.append(
                    f"[{table_id}] mapping.csv says '{csv_name}' but the CREATE script builds '{created_name}'"
                )
            tables[created_name] = {
                "table_id": table_id,
                "order": (execution_order, table_id),
                "references": {_table_name(r) for r in _REFERENCES_RE.findall(create)} - {created_name},
            }

    # Foreign-key ordering: tables are created in (execution_order, table_id)
    # order and loaded in table_id order, so every referenced table must come
    # first in both.
    for name, info in tables.items():
        for ref in sorted(info["references"]):
            target = tables.get(ref)
            if target is None:
                report.errors.append(
                    f"[{info['table_id']}] {name}: references {ref}, which is not in the migration"
                )
                continue
            if target["order"] >= info["order"]:
                report.errors.append(
                    f"[{info['table_id']}] {name}: references {ref} (table_id {target['table_id']}), "
                    "which is created later — fix execution_order"
                )
            if target["table_id"] >= info["table_id"]:
                report.errors.append(
                    f"[{info['table_id']}] {name}: references {ref} (table_id {target['table_id']}), "
                    "which is loaded later — data is loaded in table_id order"
                )

    report.tables = len(seen_ids)
    return report
