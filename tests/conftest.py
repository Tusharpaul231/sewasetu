import os
import sys
import tempfile

import psycopg2
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "app"))

DB = dict(
    host=os.environ.get("TEST_DB_HOST", "localhost"),
    port=os.environ.get("TEST_DB_PORT", "5432"),
    user=os.environ.get("TEST_DB_USER", "sewasetu"),
    password=os.environ.get("TEST_DB_PASSWORD", "sewasetu123"),
)
TEST_DB = "sewasetu_test"

# Point the app at the test database BEFORE app.py is imported.
os.environ.update({
    "DB_HOST": DB["host"], "DB_PORT": str(DB["port"]), "DB_NAME": TEST_DB,
    "DB_USER": DB["user"], "DB_PASSWORD": DB["password"],
    "SMS_GATEWAY_URL": "http://127.0.0.1:9",          # nothing listens: SMS fails fast
    "UPLOAD_DIR": os.path.join(tempfile.gettempdir(), "sewasetu-test-uploads"),
})


def _connect(dbname):
    return psycopg2.connect(dbname=dbname, **DB)


@pytest.fixture(scope="session", autouse=True)
def _database():
    admin = _connect("postgres")
    admin.autocommit = True
    cur = admin.cursor()
    cur.execute("DROP DATABASE IF EXISTS %s" % TEST_DB)
    cur.execute("CREATE DATABASE %s" % TEST_DB)
    admin.close()
    conn = _connect(TEST_DB)
    with open(os.path.join(ROOT, "app", "schema.sql"), encoding="utf-8") as fh:
        conn.cursor().execute(fh.read())
    conn.commit()
    conn.close()
    yield


@pytest.fixture(autouse=True)
def clean_tables():
    conn = _connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    tables = [r[0] for r in cur.fetchall()]
    if tables:
        cur.execute("TRUNCATE %s RESTART IDENTITY" % ",".join(tables))
    conn.commit()
    conn.close()
    yield


@pytest.fixture()
def db():
    conn = _connect(TEST_DB)
    yield conn
    conn.close()


@pytest.fixture()
def client():
    import app as app_module
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()