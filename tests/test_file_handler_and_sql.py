import pytest

import config
import db.postgresql_queries as q
import utils.file_handler as fh


def test_newlines_become_spaces_not_deleted(tmp_path):
    # Regression: deleting newlines turned "SELECT a\nFROM t" into "SELECT aFROM t".
    path = tmp_path / "q.sql"
    path.write_text("SELECT a\nFROM t\r\nWHERE\tb = 1\n")
    ok, query = fh.read_query_from_file(path)
    assert ok
    assert "a FROM t" in query and "WHERE b = 1" in query


def test_byte_order_mark_is_stripped(tmp_path):
    path = tmp_path / "bom.sql"
    path.write_bytes(b"\xef\xbb\xbfSELECT 1")
    assert fh.read_query_from_file(path) == (True, "SELECT 1")


def test_missing_files_return_tuples_not_none(tmp_path):
    assert fh.read_query_from_file(tmp_path / "nope.sql") == (False, "")
    assert fh.load_json_file(tmp_path / "nope.json") == (False, [])
    assert fh.read_json_file("x", tmp_path / "nope.json") == (False, [])


def test_invalid_json_returns_false(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json")
    assert fh.load_json_file(path) == (False, [])


@pytest.mark.parametrize("name", ["aw_sales", "_x", "Sales2025"])
def test_valid_identifiers(name):
    assert q.validate_identifier(name) == name


@pytest.mark.parametrize("name", ["", "1abc", "aw-sales", "aw sales", "x; DROP DATABASE postgres", "a" * 64])
def test_invalid_identifiers(name):
    with pytest.raises(ValueError):
        q.validate_identifier(name)


def test_render_sql_substitutes_and_escapes(monkeypatch):
    monkeypatch.setenv("DB_ROLE_PASSWORD", "it's-secret")
    monkeypatch.setattr(config, "DB_ROLE", "etl_user")
    rendered = q.render_sql("CREATE ROLE $role WITH LOGIN PASSWORD '$password';")
    assert rendered == "CREATE ROLE etl_user WITH LOGIN PASSWORD 'it''s-secret';"
    assert q.render_sql("DROP DATABASE IF EXISTS $database;", "aw_sales") == \
        "DROP DATABASE IF EXISTS aw_sales;"


def test_render_sql_rejects_unsafe_database():
    with pytest.raises(ValueError):
        q.render_sql("DROP DATABASE $database;", "x; DROP ROLE postgres")


def test_pg_query_returns_false_without_connection(monkeypatch):
    monkeypatch.setattr(q.db, "set_pg_connection", lambda *a, **k: None)
    assert q.pg_query(None, "aw_sales", "SELECT 1") is False
