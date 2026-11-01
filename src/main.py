"""
main.py — ETL Orchestration Module
==================================
Coordinates a full ETL (Extract, Transform, Load) workflow for PostgreSQL
databases.

This module automates teardown, schema creation, query mapping generation,
data extraction, and data loading into production and test environments. It is
designed to support reproducible ETL pipelines with modular components and
environment-driven configuration.

Functions:
    - Drops and rebuilds PostgreSQL databases and roles.
    - Generates source and destination query mappings from a CSV file.
    - Extracts source data using parameterized SQL SELECT queries.
    - Loads extracted data into destination tables using INSERT queries.
    - Optionally seeds a test database with the same data.

Dependencies:
    - build.build_destination_database: DDL and permission utilities.
    - extract.get_source_data: Source data extraction logic.
    - load.insert_source_data: Destination data insertion logic.
    - utils.query_mapping_handler: Mapping generation from CSV.
    - utils.logging_handler: Structured logging.
    - config: Environment/.env settings and cross-platform paths.

Environment Variables:
    - SQL_PATH: Root directory for query files and mapping CSV
      (default: <repo>/sql).
    - DB_ROLE: Role name used for PostgreSQL access control (default: etl_user).

Execution Steps:
    1. Drop existing databases.
    2. Generate source and destination query mappings.
    3. Create databases, roles, schemas, and tables.
    4. Extract source data.
    5. Load data into destination and optionally test database.

Example:
    To orchestrate ETL for the `sales_db` database and seed a test database:

    ```bash
    python src/main.py --database sales_db --seed-test-database true
    python src/main.py --database sales_db --validate-only   # no DB changes
    ```

    This will:
        - Drop and rebuild `sales_db` and `sales_db_test`.
        - Generate query mappings.
        - Extract source data.
        - Load destination tables.
"""

import argparse
import sys
import time

import pandas as pd

import build.build_destination_database as pgdb
import config
import extract.get_source_data as srcdata
import load.insert_source_data as dest
import utils.query_mapping_handler as qmh
import utils.validation_handler as vh
from utils.logging_handler import logger as log

MAPPING_FILE = config.MAPPING_FILE
SOURCE_FILE = config.SOURCE_MAPPING_FILE
DESTINATION_FILE = config.DESTINATION_MAPPING_FILE
DB_ROLE = config.DB_ROLE


def str2bool(value) -> bool:
    """
    Parse a command-line boolean.

    ``argparse`` with ``type=str`` (the previous behaviour) turned
    ``--seed-test-database False`` into the non-empty — and therefore truthy —
    string ``"False"``, so the test database was *always* seeded.
    """
    if isinstance(value, bool):
        return value
    normalised = str(value).strip().lower()
    if normalised in {"true", "t", "yes", "y", "1", "on"}:
        return True
    if normalised in {"false", "f", "no", "n", "0", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected a boolean value, got '{value}'.")


def validate_configuration(database: str) -> bool:
    """
    Pre-flight checks that run before anything is dropped: the database name
    is a safe identifier and every mapped SQL script exists and is consistent.
    """
    import db.postgresql_queries as q  # local import: keeps --help fast

    log.info("🔷 PRE-FLIGHT VALIDATION")
    try:
        q.validate_identifier(database, "database name")
        q.validate_identifier(f"{database}_test", "test database name")
        q.validate_identifier(DB_ROLE, "role name (DB_ROLE)")
    except ValueError as error:
        log.error(f"🔴 FAILED: {error}")
        return False

    report = vh.validate_mapping(MAPPING_FILE, config.SOURCE_PATH, config.DESTINATION_PATH)
    for warning in report.warnings:
        log.warning(f"🟡 WARNING: {warning}")
    for error in report.errors:
        log.error(f"🔴 FAILED: {error}")

    if report.ok:
        log.info(f"☑️ COMPLETED: Mapping valid ({report.tables} tables).")
    log.info("---------------------------------------------------------------")
    return report.ok


def main(args):
    """
    Executes the full ETL pipeline for a specified PostgreSQL database and its
    test clone.

    Order of operations (changes from the original are marked *):
        1.* Pre-flight validation and mapping generation — before anything is
            dropped, so a broken mapping can no longer destroy existing data.
        2.  Drop existing databases.
        3.* Create databases and schemas; create the ETL role if missing
            (or reset its password). The role is no longer dropped: DROP ROLE
            fails while the role holds privileges in any other database.
        4.* Create tables, *then* grant table permissions. Previously grants
            ran before any table existed, so ``GRANT ... ON ALL TABLES``
            granted nothing and the ETL role had no table access.
        5.  Extract source data and load it.
        6.* Reconcile source vs destination row counts.

    Args:
        args (argparse.Namespace): ``database`` (str), ``seed_test_database``
            (bool), ``validate_only`` (bool), ``skip_verify`` (bool).

    Raises:
        SystemExit: If any critical step in the ETL pipeline fails.
    """

    started = time.perf_counter()
    test_database = f"{args.database}_test"

    log.info("===============================================================")
    log.info(f"⚫ STARTING: ETL for Database {args.database}")

    if not validate_configuration(args.database):
        sys.exit("⛓️‍💥 EXITING: Pre-flight validation failed; nothing was changed.")

    log.info("🔷 BUILD QUERY/TABLE MAPPINGS")
    build_mapping_data("source", MAPPING_FILE, SOURCE_FILE)
    build_mapping_data("destination", MAPPING_FILE, DESTINATION_FILE)

    if args.validate_only:
        log.info("🏁 COMPLETED: Validation only — no database changes made.")
        log.info("===============================================================")
        return

    log.info("🔷 DROP DATABASES")
    drop_database(args.database)
    drop_database(test_database)

    # The ETL role is NOT dropped any more. Roles are cluster-wide, so DROP
    # ROLE failed whenever the role still held privileges in any other
    # database (e.g. one built by an earlier run under a different name),
    # aborting the whole pipeline. create_role() now creates the role if
    # missing and otherwise just resets its password.

    log.info("🔷 BUILD DATABASES")
    create_database(args.database)
    create_role(args.database)
    grant_database_permissions(args.database)
    create_database_schemas(args.database)

    create_database(test_database)
    grant_database_permissions(test_database)
    create_database_schemas(test_database)

    log.info("🔷 CREATE DATABASE TABLES")
    create_database_tables(args.database, DESTINATION_FILE)
    create_database_tables(test_database, DESTINATION_FILE)

    log.info("🔷 GRANT TABLE PERMISSIONS")
    grant_table_permissions(args.database)
    grant_table_permissions(test_database)

    log.info("🔷 EXTRACT SOURCE DATA")
    source_data = extract_source_data(SOURCE_FILE)

    log.info("🔷 LOAD DESTINATION DATA")
    load_destination_tables(args.database, DESTINATION_FILE, source_data)
    if args.seed_test_database:
        load_destination_tables(test_database, DESTINATION_FILE, source_data)

    if not args.skip_verify:
        log.info("🔷 VERIFY ROW COUNTS")
        verify_destination_tables(args.database, DESTINATION_FILE, source_data)
        if args.seed_test_database:
            verify_destination_tables(test_database, DESTINATION_FILE, source_data)

    elapsed = time.perf_counter() - started
    total_rows = sum(len(rows) for rows in source_data.values())
    log.info(
        f"🏁 COMPLETED: ETL for Database: {args.database} — "
        f"{len(source_data)} tables, {total_rows:,} rows in {elapsed:,.1f}s."
    )
    log.info("===============================================================")


def verify_destination_tables(database: str, destination_file, source_data: dict):
    """Reconcile source and destination row counts; exit on mismatch."""
    log.info(f"➡️ STARTING: Verifying {database} row counts")
    if not dest.verify_row_counts(database, destination_file, source_data):
        sys.exit(f"⛓️‍💥 EXITING: {database} row counts do not match the source.")
    log.info(f"☑️ COMPLETED: {database} row counts verified.")
    log.info("---------------------------------------------------------------")


def load_destination_tables(
        database: str,
        destination_file,
        source_data: dict):
    """
    Loads source data into PostgreSQL destination tables using predefined
    query mappings.

    This function delegates the insertion logic to `dest.insert_pg_tables`,
    which executes the mapped SQL insert statements defined in the destination
    file. It logs the start and completion of the process, and exits the
    program if the insertion fails.

    Args:
        database (str): Name of the target PostgreSQL database.
        destination_file (str): Path to the JSON file containing destination
        query mappings.
        source_data (dict): Extracted rows keyed by table_id.

    Raises:
        SystemExit: If the data insertion fails via `dest.insert_pg_tables`.
    """

    log.info("➡️ STARTING: Loading Destination Tables")
    # execute insert queries to insert source data
    success = dest.insert_pg_tables(database, destination_file, source_data)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Destination Tables not loaded.")

    log.info("☑️ COMPLETED: Destination Tables loaded.")
    log.info("---------------------------------------------------------------")


def extract_source_data(source_file) -> dict:
    """
    Extracts source data using SQL SELECT queries defined in a JSON mapping
    file.

    This function reads a JSON file containing query mappings, executes the
    mapped SQL SELECT statements, and returns the resulting data payloads.

    Args:
        source_file (str): Path to the JSON file containing source query
        mappings.

    Returns:
        dict: Extracted rows keyed by table_id.

    Raises:
        SystemExit: If no data is returned from the source queries.
    """

    # get source data
    log.info("➡️ STARTING: Extracting Source Data")
    # execute select queries to get source data
    success, source_data = srcdata.get_source_data(source_file)

    if not success:
        sys.exit("⛓️‍💥 EXITING: No source data returned.")

    log.info("☑️ COMPLETED: Source Data extracted.")
    log.info("---------------------------------------------------------------")

    return source_data


def create_database_tables(database: str, destination_file: str):
    """
    Creates PostgreSQL tables using destination query definitions.

    This function reads a JSON file containing SQL table creation queries and
    executes them against the specified PostgreSQL database to build the
    required schema.

    Args:
        database (str): Name of the target PostgreSQL database.
        destination_file (str): Path to the JSON file containing table
        creation queries.

    Raises:
        SystemExit: If table creation fails due to invalid queries or
        connection issues.
    """

    # database: execute create table queries
    log.info(f"➡️ STARTING: Creating {database} Tables.")
    success = pgdb.create_pg_tables(database, destination_file)

    if not success:
        sys.exit(f"⛓️‍💥 EXITING: {database} Tables not created.")

    log.info(f"☑️ COMPLETED: {database} Tables created.")
    log.info("---------------------------------------------------------------")


def grant_table_permissions(database) -> bool:
    """
    Grants table-level permissions for the specified PostgreSQL database.

    This function applies the necessary GRANT statements to enable access
    control for roles and users defined in the database schema.

    Args:
        database (str): Name of the target PostgreSQL database.

    Returns:
        bool: True if permissions are granted successfully.

    Raises:
        SystemExit: If permission grant fails due to invalid configuration or
        execution error.
    """

    # grant database permissions
    log.info("➡️ STARTING: Granting Table Permissions")
    success = pgdb.grant_pg_table_permissions(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Table Permissions not granted.")

    log.info("☑️ COMPLETED: Table Permissions granted.")
    log.info("---------------------------------------------------------------")


def create_database_schemas(database) -> bool:
    """
    Creates schemas for the specified PostgreSQL database.

    This function executes SQL statements to define and initialize schemas
    required for the target database.

    Args:
        database (str): Name of the target PostgreSQL database.

    Returns:
        bool: True if schemas are created successfully.

    Raises:
        SystemExit: If schema creation fails due to execution errors or
        invalid configuration.
    """
    # grant database permissions
    log.info("➡️ STARTING: Creating Database Schemas.")
    success = pgdb.create_pg_database_schemas(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Database Schemas not created.")

    log.info("☑️ COMPLETED: Database Schemas created.")
    log.info("---------------------------------------------------------------")


def grant_database_permissions(database) -> bool:
    """
    Grants database-level permissions for the specified PostgreSQL database.

    This function executes GRANT statements to assign access privileges at the
    database level, enabling role-based control over connections and
    operations.

    Args:
        database (str): Name of the target PostgreSQL database.

    Returns:
        bool: True if permissions are granted successfully.

    Raises:
        SystemExit: If permission grant fails due to configuration or
        execution errors.
    """

    # grant database permissions
    log.info("➡️ STARTING: Granting Database Permissions")
    success = pgdb.grant_pg_database_permissions(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Database Permissions not granted.")

    log.info("☑️ COMPLETED: Database Permissions granted.")
    log.info("---------------------------------------------------------------")


def create_role(database: str):
    """
    Creates a PostgreSQL role for the specified database.

    This function executes SQL statements to define a role with appropriate
    privileges for accessing and managing the target database.

    Args:
        database (str): Name of the target PostgreSQL database.

    Raises:
        SystemExit: If role creation fails due to execution errors or invalid
        configuration.
    """

    # create role
    log.info(f"➡️ STARTING: Creating Role {DB_ROLE}.")
    success = pgdb.create_pg_role(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Role not created.")

    log.info(f"☑️ COMPLETED: Role {DB_ROLE} created.")
    log.info("---------------------------------------------------------------")


def create_database(database: str):
    """
    Creates a PostgreSQL database with the specified name.

    This function executes SQL statements to initialize a new PostgreSQL
    database using the provided name.

    Args:
        database (str): Name of the database to create.

    Raises:
        SystemExit: If database creation fails due to execution errors or
        invalid configuration.
    """

    # create database
    log.info(f"➡️ STARTING: Creating Database {database}.")
    success = pgdb.create_pg_database(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Database not created.")

    log.info(f"☑️ COMPLETED: Database {database} created.")
    log.info("---------------------------------------------------------------")


def build_mapping_data(mapping_type: str, mapping_file: str, output_file: str):
    """
    Generates query or table mappings from a CSV file and writes the result to
    a JSON file.

    This function parses a CSV file containing table or query mappings and
    serializes the structured output to a JSON file. The mapping type
    determines whether the mappings are for source extraction or destination
    loading.

    Args:
        mapping_type (str): Type of mapping to generate; must be either
        'source' or 'destination'.
        mapping_file (str): Path to the CSV file containing table/query
        mappings.
        output_file (str): Path to the output JSON file where mappings will be
        written.

    Raises:
        SystemExit: If mapping generation fails due to invalid input or write
        errors.
    """

    success = False
    mapping = pd.DataFrame()
    log.info(
        f"➡️ STARTING: Building {mapping_type.title()} Query/Table Mapping."
    )

    match mapping_type:
        case "source":
            mapping = qmh.get_source_mapping_data(mapping_file)
        case "destination":
            mapping = qmh.get_destination_mapping_data(mapping_file)
        case _:
            log.error(f"FAILED: {mapping_type.title()} mapping not defined.")

    if not mapping.empty:
        success = qmh.write_mapping_data(mapping, output_file)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Query/Table Mapping failed.")

    log.info(
        f"☑️ COMPLETED: {mapping_type.title()} Query/Table Mapping completed."
    )
    log.info("---------------------------------------------------------------")


def drop_role(database: str):
    """
    Drops the PostgreSQL role associated with the specified database.

    This function executes SQL statements to remove the role tied to the given
    database, typically as part of a teardown or reinitialization process.

    Args:
        database (str): Name of the target PostgreSQL database.

    Raises:
        SystemExit: If role drop fails due to execution errors or invalid
        configuration.
    """

    log.info(f"➡️ STARTING: Dropping role {DB_ROLE}.")
    success = pgdb.drop_pg_role(database, use_default=True)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Role failed to drop.")

    log.info(f"☑️ COMPLETED: Role {DB_ROLE} dropped.")
    log.info("---------------------------------------------------------------")


def drop_database(database: str):
    """
    Drops the specified PostgreSQL database.

    This function executes SQL commands to remove the given database from the
    PostgreSQL server, typically as part of a teardown or reinitialization
    process.

    Args:
        database (str): Name of the database to drop.

    Raises:
        SystemExit: If the database drop operation fails due to execution
        errors or invalid configuration.
    """

    log.info(f"➡️ STARTING: Dropping database: {database}.")
    success = pgdb.drop_pg_database(database)

    if not success:
        sys.exit("⛓️‍💥 EXITING: Database failed to drop.")

    log.info(f"☑️ COMPLETED: Database {database} dropped.")
    log.info("---------------------------------------------------------------")


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SQL Server → PostgreSQL ETL. WARNING: drops and rebuilds "
                    "the target database and its _test clone."
    )
    parser.add_argument(
        "-d", "--database", type=str, required=True,
        help="Target PostgreSQL database name (letters, digits, underscores)."
    )
    parser.add_argument(
        "-s", "--seed-test-database", type=str2bool, nargs="?", const=True,
        default=False,
        help="Also load data into <database>_test (true/false, default false)."
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Run pre-flight checks and regenerate mappings without touching any database."
    )
    parser.add_argument(
        "--skip-verify", action="store_true",
        help="Skip the source/destination row-count reconciliation."
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    main(parse_args())
