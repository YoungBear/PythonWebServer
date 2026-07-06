def test_apispec_returns_200(client):
    resp = client.get("/apispec_1.json")
    assert resp.status_code == 200


def test_apispec_has_openapi_version(client):
    resp = client.get("/apispec_1.json")
    data = resp.get_json()
    assert data["openapi"] == "3.0.3"


def test_apispec_includes_health_path(client):
    resp = client.get("/apispec_1.json")
    data = resp.get_json()
    assert "/health" in data["paths"]


def test_apispec_includes_demo_path(client):
    from server import config

    resp = client.get("/apispec_1.json")
    data = resp.get_json()
    assert f"{config.CONTEXT_PATH}/demo/current" in data["paths"]


def test_apidocs_returns_html(client):
    resp = client.get("/apidocs/")
    assert resp.status_code == 200
    assert "text/html" in resp.content_type


def test_apidocs_contains_swagger_ui(client):
    resp = client.get("/apidocs/")
    html = resp.get_data(as_text=True)
    assert "swagger-ui" in html
    assert "/apispec_1.json" in html
