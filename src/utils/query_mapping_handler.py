"""
Module: query_mapping_handler
=============================

This module provides utilities for reading, filtering, and writing mapping data
used in ETL workflows or data migration pipelines. It supports structured
ingestion of source and destination mappings from CSV files and outputs
validated JSON records for downstream consumption.

Dependencies
------------
- pandas : For DataFrame operations and CSV/JSON I/O.
- pathlib : For file existence checks.
- utils.logging_handler.logger : Custom logger for structured error and
success reporting.

Functions
---------
- get_source_mapping_data : Extracts and filters source mapping records from a
CSV file.
- get_destination_mapping_data : Extracts and filters destination mapping
records from a CSV file.
- write_mapping_data : Serializes a DataFrame to JSON and verifies output
creation.
"""

from pathlib import Path

import pandas as pd

from utils.logging_handler import logger as log


def get_source_mapping_data(filename: str) -> pd.DataFrame:
    """
    Load and filter source mapping data from a CSV file.

    This function reads a CSV file containing source mapping definitions,
    filters for application-specific tables, and returns a sorted DataFrame
    excluding the `is_app_table` column.

    Parameters
    ----------
    filename : str
        Path to the CSV file containing source mapping data.

    Returns
    -------
    pd.DataFrame
        Filtered and sorted DataFrame with columns:
        - source_query_select
        - table_id (nullable integer)
        - execution_order

    Logging
    -------
    Logs errors if the file is not found or if any exception occurs during
    processing.

    Example
    -------
    >>> get_source_mapping_data("source_mappings.csv")
    pd.DataFrame([...])
    """
    try:
        # specify columns
        columns = [
            "source_query_select",
            "table_id",
            "execution_order",
            "is_app_table"
        ]
        # read csv file into dataframe
        df = pd.read_csv(filename, usecols=columns)
        df['table_id'] = df['table_id'].astype(pd.Int64Dtype())
        # filter data
        filtered_df = df[df['is_app_table'] == 1]
        # drop is_app_table column
        df = filtered_df.drop('is_app_table', axis=1)
        # sort data
        data = df.sort_values(by=[
            'execution_order',
            'table_id'
        ])
        return data

    except FileNotFoundError as e:
        log.error(e)
    except Exception as e:  # pylint: disable=broad-except
        log.error(e)
    # Return an empty frame (not None) so callers can safely check `.empty`.
    return pd.DataFrame()


def get_destination_mapping_data(filename: str) -> pd.DataFrame:
    """
    Load and filter destination mapping data from a CSV file.

    This function reads a CSV file containing destination mapping definitions,
    filters for application-specific tables, and returns a sorted DataFrame
    excluding the `is_app_table` column.

    Parameters
    ----------
    filename : str
        Path to the CSV file containing destination mapping data.

    Returns
    -------
    pd.DataFrame
        Filtered and sorted DataFrame with columns:
        - destination_query_create
        - destination_query_insert
        - table_id (nullable integer)
        - execution_order

    Logging
    -------
    Logs errors with traceback if the file is not found or if any exception
    occurs.

    Example
    -------
    >>> get_destination_mapping_data("destination_mappings.csv")
    pd.DataFrame([...])
    """
    try:
        # specify columns
        columns = [
            "destination_query_create",
            "destination_query_insert",
            "table_id",
            "execution_order",
            "is_app_table",
        ]
        # read csv file into dataframe
        df = pd.read_csv(filename, usecols=columns)
        df['table_id'] = df['table_id'].astype(pd.Int64Dtype())
        # filter data
        filtered_df = df[df['is_app_table'] == 1]
        # drop is_app_table column
        df = filtered_df.drop('is_app_table', axis=1)
        # sort data
        data = df.sort_values(
            by=["execution_order", "table_id"]
        )
        return data
    except FileNotFoundError as e:
        log.error(e, exc_info=True)
    except Exception as e:  # pylint: disable=broad-except
        log.error(e, exc_info=True)
    # Return an empty frame (not None) so callers can safely check `.empty`.
    return pd.DataFrame()


def write_mapping_data(data: pd.DataFrame, output_filename: str) -> bool:
    """
    Write mapping data to a JSON file and confirm output creation.

    This function serializes the provided DataFrame to a JSON file using
    record orientation. It verifies that the file was successfully created
    and logs a success message with the filename.

    Parameters
    ----------
    data : pd.DataFrame
        The mapping data to be written to disk.
    output_filename : str
        The target filename for the JSON output.

    Returns
    -------
    bool
        True if the file was successfully created, False otherwise.

    Logging
    -------
    Logs success with filename if output is created.
    Logs errors with traceback if any exception occurs.

    Example
    -------
    >>> write_mapping_data(df, "output.json")
    True
    """
    success = False

    try:
        # write mapping data to output filename
        output = Path(output_filename)
        data.to_json(output, orient="records", indent=2)
        success = output.is_file()

        if success:
            log.info(f"🟢 SUCCESS: {output.name} created.")

        return success

    except Exception as e:  # pylint: disable=broad-except
        log.error(e, exc_info=True)
        return False
