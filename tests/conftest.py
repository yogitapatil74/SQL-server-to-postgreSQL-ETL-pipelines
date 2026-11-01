"""
Test configuration.

- Puts ``src/`` on the import path (the application uses top-level imports
  such as ``import config``).
- Sends log files to a temporary directory.
- Provides minimal stand-ins for ``psycopg2`` when it is not installed, so
  the unit tests (which never touch a real database) can run anywhere. With
  ``psycopg2-binary`` installed, as in CI, the real package is used.
"""

import os
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("LOGS_PATH", tempfile.mkdtemp(prefix="etl-test-logs-"))
os.environ.setdefault("POSTGRES_DB_USERNAME", "test_user")
os.environ.setdefault("DB_ROLE_PASSWORD", "test-password")

try:  # pragma: no cover - depends on environment
    import psycopg2  # noqa: F401
except ImportError:  # pragma: no cover
    psycopg2 = types.ModuleType("psycopg2")

    class Error(Exception):
        pass

    class OperationalError(Error):
        pass

    def connect(*args, **kwargs):
        raise OperationalError("psycopg2 stub: no database available in tests")

    psycopg2.Error = Error
    psycopg2.OperationalError = OperationalError
    psycopg2.IntegrityError = Error
    psycopg2.connect = connect

    extras = types.ModuleType("psycopg2.extras")
    extras.execute_batch = lambda cursor, query, values, page_size=100: None

    sql = types.ModuleType("psycopg2.sql")

    class Composable:
        def __init__(self, *parts):
            self.parts = parts

        def format(self, *args):
            return Composable(self.parts, args)

    sql.SQL = Composable
    sql.Identifier = Composable

    psycopg2.extras = extras
    psycopg2.sql = sql
    sys.modules["psycopg2"] = psycopg2
    sys.modules["psycopg2.extras"] = extras
    sys.modules["psycopg2.sql"] = sql
