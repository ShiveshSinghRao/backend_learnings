from fastapi.testclient import TestClient

from learn_backend.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_expected_body():
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data


def test_docs_page_accessible():
    """FastAPI auto-generates docs at /docs."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_unknown_route_returns_404():
    response = client.get("/this-does-not-exist")
    assert response.status_code == 404
