"""
Integration test against a real PostgreSQL server (no SQL Server needed).

Runs the whole pipeline — pre-flight, drop, create database/role/schemas,
all 35 CREATE TABLE scripts, grants, load, row-count verification — with a
handful of synthetic source rows standing in for the SQL Server extract.

Skipped unless ETL_PG_INTEGRATION=1. Needs the PostgreSQL settings from
.env.example (POSTGRESQL_HOSTNAME, POSTGRES_DB_USERNAME, ...), pointing at a
throwaway server: it DROPS and recreates the target databases and role.
"""

import json
import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("ETL_PG_INTEGRATION") != "1",
    reason="set ETL_PG_INTEGRATION=1 to run against a real PostgreSQL server",
)

DATABASE = os.getenv("ETL_PG_TEST_DATABASE", "etl_ci")

ROWS = {
    1: [(1, "Billing", "b3f0a2c4-0000-4000-8000-000000000001", "2008-04-30 00:00:00"),
        (2, "Home", "b3f0a2c4-0000-4000-8000-000000000002", "2008-04-30 00:00:00")],
    2: [("AU", "Australia", "2008-04-30 00:00:00"), ("IN", "India", "2008-04-30 00:00:00")],
    3: [(1, "Cell", "2017-12-13 13:19:22")],
    9: [("AUD", "Australian Dollar", "2008-04-30 00:00:00")],
    10: [(1, "Price", "Other", "2008-04-30 00:00:00")],
}


def _source_data(config):
    with open(config.DESTINATION_MAPPING_FILE, encoding="utf-8") as handle:
        entries = json.load(handle)
    return {int(e["table_id"]): ROWS.get(int(e["table_id"]), []) for e in entries}


def test_full_pipeline_against_postgres(monkeypatch):
    import config
    import db.postgresql_queries as q
    import main

    data = _source_data(config)
    monkeypatch.setattr(main, "extract_source_data", lambda source_file: data)

    main.main(main.parse_args(["-d", DATABASE, "-s", "true"]))

    for database in (DATABASE, f"{DATABASE}_test"):
        assert q.pg_scalar(database, "SELECT count(*) FROM people.address_types") == 2
        # modified_date used to be a TIME column here, silently dropping the date.
        assert str(q.pg_scalar(database, "SELECT modified_date FROM sales.currencies")).startswith("2008-04-30")
        tables = q.pg_scalar(
            database,
            "SELECT count(*) FROM information_schema.tables "
            "WHERE table_schema IN ('people', 'production', 'sales')",
        )
        assert tables == 35


def test_etl_role_can_read_and_write_tables(monkeypatch):
    """Regression: grants used to run before the tables existed."""
    import config
    import db.postgresql as pg

    monkeypatch.setenv("POSTGRES_DB_USERNAME", config.DB_ROLE)
    monkeypatch.setenv("POSTGRES_DB_PASSWORD", config.require("DB_ROLE_PASSWORD"))
    conn = pg.set_pg_connection(DATABASE)
    assert conn is not None, "ETL role could not connect"
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM people.country_regions")
            assert cursor.fetchone()[0] == 2
            cursor.execute(
                "INSERT INTO sales.sales_reasons OVERRIDING SYSTEM VALUE "
                "VALUES (99, 'CI', 'Other', now())"
            )
    finally:
        conn.close()
