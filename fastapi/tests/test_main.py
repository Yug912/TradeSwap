from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_match_accepts_valid_request() -> None:
    response = client.post(
        "/match",
        json={
            "user_id": 1,
            "teach": [
                {"skill": "Python", "level": "advanced"},
                {"skill": "C++", "level": "intermediate"},
            ],
            "learn": [{"skill": "Machine Learning", "level": "beginner"}],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"matches": []}


def test_match_rejects_invalid_request() -> None:
    response = client.post(
        "/match",
        json={"user_id": "not-an-integer", "teach": [], "learn": []},
    )

    assert response.status_code == 422