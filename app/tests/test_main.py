from fastapi.testclient import TestClient

from app.main import app


def test_book_car_when_no_available_cars():
    """Test book car when no available cars"""
    client = TestClient(app)
    response = client.post(
        "/api/book", json={"source": {"x": 0, "y": 0}, "destination": {"x": 1, "y": 1}}
    )
    assert response.status_code == 204


def test_book_car():
    """Test book car"""
    client = TestClient(app)
    client.put("/api/reset")

    response = client.post(
        "/api/book", json={"source": {"x": 0, "y": 0}, "destination": {"x": 1, "y": 1}}
    )
    assert response.status_code == 201
    assert response.json()["car_id"] == 1


def test_tick():
    """Test tick, increment current time"""
    client = TestClient(app)
    client.put("/api/reset")

    client.post("/api/tick")
    client.post("/api/tick")
    client.post("/api/tick")
    client.post("/api/tick")
    response = client.post("/api/tick")

    assert response.json()["current_time"] == 5


def test_reset():
    """Test reset"""
    client = TestClient(app)
    client.put("/api/reset")

    client.post("/api/tick")
    client.post("/api/tick")
    client.post("/api/tick")
    client.post("/api/tick")
    response = client.post("/api/tick")

    assert response.json()["current_time"] == 5

    response = client.put("/api/reset")
    assert response.json()["current_time"] == 0
