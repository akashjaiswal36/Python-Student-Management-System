import pytest, asyncio, httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from fastapi.testclient import TestClient

# Use an in‑memory SQLite for tests
SQLALCHEMY_TEST_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)

# Dependency override
def override_db():
    db = TestingSession()
    try:   yield db
    finally: db.close()

app.dependency_overrides[get_db] = override_db
client = TestClient(app)

def test_crud_flow():
    # Create
    r = client.post("/api/students", json={"id": 1, "name": "Alice", "course": "Math"})
    assert r.status_code == 201
    # Get all
    r = client.get("/api/students")
    assert any(s["name"] == "Alice" for s in r.json())
    # Delete
    r = client.delete("/api/students/1")
    assert r.status_code == 200
