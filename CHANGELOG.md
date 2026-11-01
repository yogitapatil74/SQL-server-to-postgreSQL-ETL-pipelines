# Changelog

## 0.2.0 — Bug fixes and enhancements

### Critical bugs fixed

- **Rows could be loaded into the wrong tables.** Extraction appended each
  table's rows to a list but skipped tables that returned no rows; loading then
  read `data[table_id - 1]`. One empty source table shifted every later table's
  data by one position (wrong table, or an `IndexError`). Rows are now keyed by
  `table_id`.
- **Failed loads were reported as successful.** `insert_pg_tables` set
  `success = True` after every INSERT whatever the result, so constraint or type
  errors were logged as "SUCCESS" and the run "COMPLETED". Every insert result
  is now checked, and the run stops with a non-zero exit code.
- **`--seed-test-database False` still seeded the test database.** The flag was
  parsed with `type=str`, and the non-empty string `"False"` is truthy. It is now
  parsed as a real boolean (and defaults to `false`).
- **The ETL role never had table permissions.** Table grants ran before any table
  existed, so `GRANT … ON ALL TABLES` granted nothing, and default privileges
  covered only the empty `public` schema. Grants now run after the tables are
  created, and default privileges cover `people`, `production` and `sales`.
- **Dates were silently dropped in 3 tables.** `modified_date` was a `time`
  column in `sales.currencies`, `sales.sales_person_credit_cards` and
  `sales.sales_territories_history`, so `2008-04-30 00:00:00` was stored as
  `00:00:00`. These columns are now `timestamp`.
- **A broken mapping destroyed existing data.** Databases were dropped *before*
  checking that the SQL scripts existed. A new pre-flight validation runs first
  and exits without changing anything if a problem is found.
- **Only ran on Windows.** Every path was built with `\\` separators, and
  `CREATE DATABASE` hard-coded the Windows-only collation
  `English_United States.1252`. Paths now use `pathlib` and default to the
  repository, and the database is created with portable settings.

### Other bugs fixed

- Re-running with a different database name failed: `DROP ROLE` errors while the
  role still holds privileges in another database. The role is now created if
  missing (or its password reset) instead of being dropped.
- `create_pg_tables` returned only the *last* table's result (earlier failures
  were ignored) and crashed with `IndexError` if fewer than two tables were mapped.
- Many functions returned `None` from `except` blocks, so callers unpacking
  `success, data = …` crashed with `TypeError` instead of logging the error.
- SQL scripts were read with newlines *deleted* (`SELECT a\nFROM t` → `SELECT aFROM t`).
  They are now replaced with spaces, and a UTF-8 BOM is stripped.
- A role password containing `'` broke `CREATE ROLE`; it is now escaped.
- The `--database` value was pasted into `DROP/CREATE DATABASE` unchecked; it
  must now be a plain identifier.
- `pg_query` crashed on a failed connection (`None.cursor()`), had a mutable
  default argument, and substituted `$password` *after* executing the query (dead code).
- SQL Server queries that returned zero rows were treated as failures.
- A missing `mapping.csv` returned `None` and crashed with `AttributeError` on `.empty`.
- The role name was hard-coded as `etl_user` in SQL even though `DB_ROLE` was configurable.
- `ALTER TABLE … OWNER to postgres` failed when the admin user was not called `postgres`.
- `mapping.csv` named table 28 `sales_sales_people_quota_history`; the real table is `sales_people_quota_history`.
- `error.log` had no timestamp format, and an invalid `LOG_LEVEL` passed `None` to the handlers.
- README told you to run `python3 -m main.py`, which does not work.
- `.env example` (with a space) renamed to `.env.example`.

### Enhancements

- `--validate-only`: checks every mapped script exists and is non-empty, that the
  INSERT column, placeholder and SELECT column counts agree, that INSERT and CREATE
  target the same table, and that foreign keys are created and loaded in order.
  It does this without connecting to any database.
- Row-count reconciliation after loading (`--skip-verify` to disable).
- Each table loads in a single transaction, so a failure rolls the table back
  instead of leaving it half-loaded.
- `INSERT_PAGE_SIZE` is configurable (default raised from 100 to 1000 rows per batch).
- One SQL Server connection is reused for all source queries.
- Run summary with the table count, row count and elapsed time.
- Test suite: 55 unit tests, plus 2 integration tests that run the full pipeline
  against real PostgreSQL. A `docker-compose.yml` provides a local PostgreSQL, and
  CI is in GitHub Actions.
- Dependencies cleaned up: removed `argparse` (part of the standard library) and
  `python-decouple`, moved black and sphinx out of the runtime dependencies,
  switched to `psycopg2-binary`, and widened Python support to `>=3.10`.
  `pdm.lock` was removed because it no longer matched; run `pdm lock` to regenerate it.
