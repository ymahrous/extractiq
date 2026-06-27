import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from models import User, Document, Extraction
from database import get_session
from main import app
from fastapi.testclient import TestClient
from auth import get_password_hash

# 2. Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

# 3. Create tables
def init_test_db():
    SQLModel.metadata.create_all(engine)

# 4. Override the dependency injection in FastAPI
def override_get_session():
    yield Session(engine)

# 5. Create a fixture to give us a clean database for every single test
@pytest.fixture(autouse=True)
def db_session():
    init_test_db()
    yield Session(engine)
    # Teardown: Drop all data after every test
    SQLModel.metadata.drop_all(engine)

# 6. Create a fixture for the FastAPI client (acts like a browser)
@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c