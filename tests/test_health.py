def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_returns_up_status(client):
    resp = client.get("/health")
    data = resp.get_json()
    assert data["status"] == "UP"


def test_health_has_timestamp(client):
    resp = client.get("/health")
    data = resp.get_json()
    assert "timestamp" in data
    assert data["timestamp"].isdigit()


def test_health_response_is_json(client):
    resp = client.get("/health")
    assert resp.content_type == "application/json"
