from server import config


def test_demo_current_returns_200(client):
    resp = client.get(f"{config.CONTEXT_PATH}/demo/current")
    assert resp.status_code == 200


def test_demo_current_has_zoned_date_time(client):
    resp = client.get(f"{config.CONTEXT_PATH}/demo/current")
    data = resp.get_json()
    assert "zonedDateTime" in data
    assert "+00:00" in data["zonedDateTime"]


def test_demo_current_has_timestamp(client):
    resp = client.get(f"{config.CONTEXT_PATH}/demo/current")
    data = resp.get_json()
    assert "timestamp" in data
    assert data["timestamp"].isdigit()


def test_demo_current_is_json(client):
    resp = client.get(f"{config.CONTEXT_PATH}/demo/current")
    assert resp.content_type == "application/json"
