from pathlib import Path

import config
from utils.validation_handler import count_select_columns, validate_mapping

HEADER = (
    "execution_order,is_app_table,table_id,source_schema,source_table,source_query_select,"
    "source_query_select_tested,destination_schema,destination_table,destination_query_create,"
    "destination_query_create_tested,destination_query_insert,destination_query_insert_tested\n"
)


def make_project(tmp_path: Path, tables):
    """tables: list of (order, id, name, create_sql, insert_sql, select_sql)."""
    src, dst = tmp_path / "source", tmp_path / "destination"
    src.mkdir()
    dst.mkdir()
    lines = [HEADER]
    for order, table_id, name, create, insert, select in tables:
        (src / f"S.{name}__SELECT.sql").write_text(select)
        (dst / f"s.{name}__CREATE.sql").write_text(create)
        (dst / f"s.{name}__INSERT.sql").write_text(insert)
        lines.append(
            f"{order},1,{table_id},S,{name},S.{name}__SELECT.sql,,s,{name},"
            f"s.{name}__CREATE.sql,,s.{name}__INSERT.sql,\n"
        )
    mapping = tmp_path / "mapping.csv"
    mapping.write_text("".join(lines))
    return mapping, src, dst


def table(name, refs=None, columns=2, select_columns=None):
    ref_sql = f", CONSTRAINT fk FOREIGN KEY (b) REFERENCES s.{refs} (a)" if refs else ""
    cols = ", ".join(f"c{i}" for i in range(columns))
    marks = ", ".join(["%s"] * columns)
    sel = ", ".join(f"[c{i}]" for i in range(select_columns or columns))
    return (
        f"CREATE TABLE IF NOT EXISTS s.{name} (a int, b int{ref_sql});",
        f"INSERT INTO s.{name} ({cols}) VALUES ({marks});",
        f"SELECT {sel} FROM [S].[{name}]",
    )


def test_repository_mapping_is_valid():
    report = validate_mapping(config.MAPPING_FILE, config.SOURCE_PATH, config.DESTINATION_PATH)
    assert report.ok, report.errors
    assert report.tables == 35
    assert report.warnings == []


def test_valid_project(tmp_path):
    mapping, src, dst = make_project(tmp_path, [
        (0, 1, "parent", *table("parent")),
        (1, 2, "child", *table("child", refs="parent")),
    ])
    assert validate_mapping(mapping, src, dst).ok


def test_missing_script_is_an_error(tmp_path):
    mapping, src, dst = make_project(tmp_path, [(0, 1, "t", *table("t"))])
    (dst / "s.t__INSERT.sql").unlink()
    report = validate_mapping(mapping, src, dst)
    assert not report.ok
    assert any("missing destination_query_insert" in e for e in report.errors)


def test_placeholder_mismatch_is_an_error(tmp_path):
    create, _, select = table("t")
    mapping, src, dst = make_project(tmp_path, [
        (0, 1, "t", create, "INSERT INTO s.t (c0, c1) VALUES (%s);", select),
    ])
    report = validate_mapping(mapping, src, dst)
    assert any("2 columns but has 1 placeholders" in e for e in report.errors)


def test_select_column_mismatch_is_an_error(tmp_path):
    mapping, src, dst = make_project(tmp_path, [(0, 1, "t", *table("t", select_columns=3))])
    report = validate_mapping(mapping, src, dst)
    assert any("SELECT returns 3 columns but INSERT expects 2" in e for e in report.errors)


def test_foreign_key_loaded_too_late_is_an_error(tmp_path):
    mapping, src, dst = make_project(tmp_path, [
        (0, 1, "child", *table("child", refs="parent")),
        (0, 2, "parent", *table("parent")),
    ])
    report = validate_mapping(mapping, src, dst)
    assert any("loaded later" in e for e in report.errors)


def test_duplicate_table_id_is_an_error(tmp_path):
    mapping, src, dst = make_project(tmp_path, [
        (0, 1, "a", *table("a")),
        (0, 1, "b", *table("b")),
    ])
    assert any("duplicate table_id" in e for e in validate_mapping(mapping, src, dst).errors)


def test_count_select_columns_ignores_nested_commas():
    query = "SELECT [a], [b] = CAST(b AS DECIMAL(18,2)), CONVERT(VARCHAR(36), c) FROM t"
    assert count_select_columns(query) == 3
    assert count_select_columns("CREATE TABLE x (a int)") is None
