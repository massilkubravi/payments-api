import os
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Use separate test database
test_database_url = os.getenv("TEST_DATABASE_URL")

if not test_database_url:
    raise RuntimeError("Set TEST_DATABASE_URL before running tests")

os.environ["DATABASE_URL"] = test_database_url

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client