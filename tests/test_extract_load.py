import json
from unittest.mock import MagicMock

import pytest

import build.build_destination_database as build
import extract.get_source_data as extract
import load.insert_source_data as load


@pytest.fixture
def project(tmp_path, monkeypatch):
    src, dst = tmp_path / "source", tmp_path / "destination"
    src.mkdir()
    dst.mkdir()
    entries = []
    for table_id, name in [(1, "a"), (2, "b"), (3, "c")]:
        (src / f"{name}.sql").write_text(f"SELECT x, y FROM {name}")
        (dst / f"{name}__CREATE.sql").write_text(f"CREATE TABLE s.{name} (x int, y int);")
        (dst / f"{name}__INSERT.sql").write_text(f"INSERT INTO s.{name} (x, y) VALUES (%s, %s);")
        entries.append({
            "table_id": table_id, "execution_order": 0,
            "source_query_select": f"{name}.sql",
            "destination_query_create": f"{name}__CREATE.sql",
            "destination_query_insert": f"{name}__INSERT.sql",
        })
    source_json = tmp_path / "mapping_source.json"
    dest_json = tmp_path / "mapping_destination.json"
    source_json.write_text(json.dumps(entries))
    dest_json.write_text(json.dumps(list(reversed(entries))))  # order must not matter
    monkeypatch.setattr(extract, "SOURCE_PATH", src)
    monkeypatch.setattr(load, "DESTINATION_PATH", dst)
    monkeypatch.setattr(build, "DESTINATION_PATH", dst)
    return source_json, dest_json


def test_extract_keys_rows_by_table_id_even_with_empty_table(project, monkeypatch):
    source_json, _ = project
    results = {"a": [(1, 1)], "b": [], "c": [(3, 3), (4, 4)]}
    conn = MagicMock()
    monkeypatch.setattr(extract.sqldb, "connect_sql_server", lambda: conn)
    monkeypatch.setattr(
        extract.sqldb, "execute_sql_query",
        lambda c, query: (True, results[query.split()[-1]]),
    )
    ok, data = extract.get_source_data(source_json)
    # Regression: an empty table used to shift every later table's rows by one.
    assert ok
    assert data == {1: [(1, 1)], 2: [], 3: [(3, 3), (4, 4)]}
    conn.close.assert_called_once()


def test_extract_fails_on_query_error(project, monkeypatch):
    source_json, _ = project
    monkeypatch.setattr(extract.sqldb, "connect_sql_server", lambda: MagicMock())
    monkeypatch.setattr(extract.sqldb, "execute_sql_query", lambda c, q: (False, []))
    assert extract.get_source_data(source_json) == (False, {})


def test_load_sends_each_tables_rows_to_its_own_insert(project, monkeypatch):
    _, dest_json = project
    sent = []
    monkeypatch.setattr(load.pgdb, "set_pg_connection", lambda db: MagicMock())
    monkeypatch.setattr(
        load.q, "pg_query",
        lambda conn, database, query, values: sent.append((query.split()[2], values)) or True,
    )
    data = {1: [(1, 1)], 2: [], 3: [(3, 3)]}
    assert load.insert_pg_tables("aw_sales", dest_json, data) is True
    assert sent == [("s.a", [(1, 1)]), ("s.c", [(3, 3)])]  # empty table 2 skipped


def test_load_reports_failure_instead_of_success(project, monkeypatch):
    # Regression: success was hard-coded to True after every insert.
    _, dest_json = project
    monkeypatch.setattr(load.pgdb, "set_pg_connection", lambda db: MagicMock())
    monkeypatch.setattr(load.q, "pg_query", lambda *a, **k: False)
    assert load.insert_pg_tables("aw_sales", dest_json, {1: [(1, 1)], 2: [(2, 2)], 3: [(3, 3)]}) is False


def test_load_rejects_wrong_row_shape(project, monkeypatch):
    _, dest_json = project
    monkeypatch.setattr(load.pgdb, "set_pg_connection", lambda db: MagicMock())
    monkeypatch.setattr(load.q, "pg_query", lambda *a, **k: True)
    assert load.insert_pg_tables("aw_sales", dest_json, {1: [(1, 2, 3)], 2: [], 3: []}) is False


def test_load_fails_when_a_table_was_not_extracted(project, monkeypatch):
    _, dest_json = project
    assert load.insert_pg_tables("aw_sales", dest_json, {1: [(1, 1)]}) is False


def test_verify_row_counts(project, monkeypatch):
    _, dest_json = project
    counts = iter([1, 0, 2])
    monkeypatch.setattr(load.q, "pg_scalar", lambda db, query: next(counts))
    assert load.verify_row_counts("aw_sales", dest_json, {1: [(1, 1)], 2: [], 3: [(3, 3), (4, 4)]})

    counts = iter([1, 0, 1])
    assert not load.verify_row_counts("aw_sales", dest_json, {1: [(1, 1)], 2: [], 3: [(3, 3), (4, 4)]})


def test_create_tables_stops_at_first_failure(project, monkeypatch):
    # Regression: only the last table's result was returned.
    _, dest_json = project
    results = iter([True, False, True])
    executed = []
    monkeypatch.setattr(build.db, "set_pg_connection", lambda *a, **k: MagicMock())
    monkeypatch.setattr(
        build.q, "pg_query", lambda conn, db, query: executed.append(query) or next(results)
    )
    assert build.create_pg_tables("aw_sales", dest_json) is False
    assert len(executed) == 2
