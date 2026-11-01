import argparse

import pytest

import main


@pytest.mark.parametrize("value", ["true", "True", "YES", "y", "1", "on"])
def test_str2bool_true(value):
    assert main.str2bool(value) is True


@pytest.mark.parametrize("value", ["false", "False", "NO", "n", "0", "off"])
def test_str2bool_false(value):
    assert main.str2bool(value) is False


def test_str2bool_rejects_garbage():
    with pytest.raises(argparse.ArgumentTypeError):
        main.str2bool("maybe")


def test_seed_flag_false_string_is_false():
    # Regression: type=str made "False" truthy, so the test DB was always seeded.
    args = main.parse_args(["-d", "aw_sales", "--seed-test-database", "False"])
    assert args.seed_test_database is False


def test_seed_flag_defaults_and_bare_flag():
    assert main.parse_args(["-d", "aw_sales"]).seed_test_database is False
    assert main.parse_args(["-d", "aw_sales", "-s"]).seed_test_database is True


def _record_steps(monkeypatch, validation_ok=True):
    calls = []
    monkeypatch.setattr(main, "validate_configuration", lambda db: calls.append(("validate", db)) or validation_ok)
    for name in [
        "build_mapping_data", "drop_database", "drop_role", "create_database",
        "create_role", "grant_database_permissions", "create_database_schemas",
        "create_database_tables", "grant_table_permissions", "load_destination_tables",
        "verify_destination_tables",
    ]:
        monkeypatch.setattr(main, name, lambda *a, _n=name, **k: calls.append((_n, a[0] if a else None)))
    monkeypatch.setattr(main, "extract_source_data", lambda f: calls.append(("extract", None)) or {1: [(1,)]})
    return calls


def test_grants_run_after_tables_exist(monkeypatch):
    calls = _record_steps(monkeypatch)
    main.main(main.parse_args(["-d", "aw_sales", "-s", "true"]))
    names = [c[0] for c in calls]

    for db in ("aw_sales", "aw_sales_test"):
        create = calls.index(("create_database_tables", db))
        grant = calls.index(("grant_table_permissions", db))
        assert create < grant, f"table grants must run after CREATE TABLE for {db}"

    assert ("load_destination_tables", "aw_sales_test") in calls
    assert names.count("verify_destination_tables") == 2


def test_test_database_not_seeded_when_false(monkeypatch):
    calls = _record_steps(monkeypatch)
    main.main(main.parse_args(["-d", "aw_sales", "-s", "false"]))
    assert ("load_destination_tables", "aw_sales_test") not in calls


def test_failed_validation_exits_before_dropping_anything(monkeypatch):
    calls = _record_steps(monkeypatch, validation_ok=False)
    with pytest.raises(SystemExit):
        main.main(main.parse_args(["-d", "aw_sales"]))
    assert not any(name.startswith("drop") for name, _ in calls)


def test_validate_only_makes_no_database_changes(monkeypatch):
    calls = _record_steps(monkeypatch)
    main.main(main.parse_args(["-d", "aw_sales", "--validate-only"]))
    assert [c[0] for c in calls] == ["validate", "build_mapping_data", "build_mapping_data"]


def test_validate_configuration_rejects_unsafe_database_name():
    assert main.validate_configuration("aw_sales; DROP DATABASE postgres") is False


def test_validate_configuration_accepts_repo_mapping():
    assert main.validate_configuration("aw_sales") is True


def test_build_mapping_data_writes_json(tmp_path):
    import json

    import config

    out = tmp_path / "mapping_destination.json"
    main.build_mapping_data("destination", config.MAPPING_FILE, out)
    entries = json.loads(out.read_text())
    assert len(entries) == 35
    assert {"table_id", "destination_query_create", "destination_query_insert"} <= set(entries[0])


def test_build_mapping_data_unknown_type_exits(tmp_path):
    import config

    with pytest.raises(SystemExit):
        main.build_mapping_data("bogus", config.MAPPING_FILE, tmp_path / "x.json")
