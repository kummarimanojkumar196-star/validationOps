import pytest
from fastapi.testclient import TestClient

from validationops.api import main
from validationops.api.main import app

client = TestClient(app)


def test_health_all_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "check_db", lambda: True)
    monkeypatch.setattr(main, "check_redis", lambda: True)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok", "redis": "ok"}


def test_health_redis_down(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "check_db", lambda: True)
    monkeypatch.setattr(main, "check_redis", lambda: False)

    response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["db"] == "ok"
    assert body["redis"] == "down"
