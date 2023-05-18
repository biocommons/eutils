import pytest


def test_import_client():
    try:
        # flake8: noqa
        from eutils import Client
    except Exception:
        pytest.fail("Client was unable to be imported")

def test_import_exceptions():
    try:
        # flake8: noqa
        from eutils import EutilsError, EutilsNCBIError, EutilsNotFoundError, EutilsRequestError
    except Exception as exc:
        pytest.fail(f"An exception was unable to be imported: {exc}")

def test_import_sqllitecache():
    try:
        # flake8: noqa
        from eutils import SQLiteCache
    except Exception:
        pytest.fail("SQLiteCache was unable to be imported")

def test_import_queryservice():
    try:
        # flake8: noqa
        from eutils import QueryService
    except Exception:
        pytest.fail("QueryService was unable to be imported")

def test_import_warnings():
    try:
        # flake8: noqa
        from eutils import warnings
    except Exception:
        pytest.fail("warnings were unable to be imported")