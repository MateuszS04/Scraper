import sys
from pathlib import Path

import pytest
import requests

# Ensure project root is on sys.path so 'scrapers' package can be imported in tests
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storage.db import init_db, save_screenshot

def test_init_db():
    try:
        init_db()
    except Exception as e:
        pytest.fail(f"init_db() raised an exception: {e}")