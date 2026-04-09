import importlib
import sys
from pathlib import Path

# Ensure project root is on sys.path so 'storage' package can be imported in tests
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import storage.db_config as db_config_module


def _reload_db_config():
    return importlib.reload(db_config_module)


def test_db_config_reads_values_from_environment(monkeypatch):
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "secret")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "scraper_test")

    mod = _reload_db_config()

    assert mod.dbConfig.DB_USER == "test_user"
    assert mod.dbConfig.DB_PASSWORD == "secret"
    assert mod.dbConfig.DB_HOST == "localhost"
    assert mod.dbConfig.DB_PORT == "5432"
    assert mod.dbConfig.DB_NAME == "scraper_test"


def test_db_config_uses_none_when_variables_missing(monkeypatch):
    import dotenv

    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_PASSWORD", raising=False)
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.delenv("DB_PORT", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    # Prevent .env from repopulating values during module reload.
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *args, **kwargs: None)

    mod = _reload_db_config()

    assert mod.dbConfig.DB_USER is None
    assert mod.dbConfig.DB_PASSWORD is None
    assert mod.dbConfig.DB_HOST is None
    assert mod.dbConfig.DB_PORT is None
    assert mod.dbConfig.DB_NAME is None