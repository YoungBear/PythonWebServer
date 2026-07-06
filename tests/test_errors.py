def test_404_returns_json(client):
    resp = client.get("/nonexistent")
    assert resp.status_code == 404
    assert resp.content_type == "application/json"


def test_404_body_has_error_fields(client):
    resp = client.get("/nonexistent")
    data = resp.get_json()
    assert "error" in data
    assert "status" in data
    assert data["status"] == 404


def test_method_not_allowed(client):
    resp = client.post("/health")
    assert resp.status_code == 405
    assert resp.content_type == "application/json"
