import pytest

from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_FILE", str(tmp_path / "expenses.json"))
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_add_and_list(client):
    res = client.post("/expenses", json={"amount": 250, "category": "Travel", "note": "bus"})
    assert res.status_code == 201
    assert res.get_json()["category"] == "travel"

    items = client.get("/expenses").get_json()
    assert len(items) == 1
    assert items[0]["amount"] == 250


@pytest.mark.parametrize(
    "payload",
    [{}, {"amount": -5, "category": "food"}, {"amount": "abc", "category": "food"}, {"amount": 5}],
)
def test_bad_input_returns_400(client, payload):
    res = client.post("/expenses", json=payload)
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_summary(client):
    client.post("/expenses", json={"amount": 100, "category": "food"})
    client.post("/expenses", json={"amount": 50.5, "category": "food"})
    client.post("/expenses", json={"amount": 200, "category": "travel"})
    data = client.get("/summary").get_json()
    assert data["by_category"] == {"food": 150.5, "travel": 200}
    assert data["total"] == 350.5


def test_version_comes_from_environment(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    assert client.get("/version").get_json() == {"version": "1.2.3"}


def test_version_defaults_to_dev(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert client.get("/version").get_json() == {"version": "dev"}
