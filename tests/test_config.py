import importlib

import pytest

from server import config


@pytest.fixture(autouse=True)
def _restore_config():
    yield
    importlib.reload(config)


def test_context_path_default(monkeypatch):
    monkeypatch.delenv("CONTEXT_PATH", raising=False)
    importlib.reload(config)
    assert config.CONTEXT_PATH == "/PythonWebServer"


def test_context_path_adds_leading_slash(monkeypatch):
    monkeypatch.setenv("CONTEXT_PATH", "PythonWebServer")
    importlib.reload(config)
    assert config.CONTEXT_PATH == "/PythonWebServer"


def test_context_path_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("CONTEXT_PATH", "/PythonWebServer/")
    importlib.reload(config)
    assert config.CONTEXT_PATH == "/PythonWebServer"


def test_context_path_root(monkeypatch):
    monkeypatch.setenv("CONTEXT_PATH", "/")
    importlib.reload(config)
    assert config.CONTEXT_PATH == "/"


def test_context_path_empty(monkeypatch):
    monkeypatch.setenv("CONTEXT_PATH", "")
    importlib.reload(config)
    assert config.CONTEXT_PATH == "/"


def test_verify_client_cert_defaults_true(monkeypatch):
    monkeypatch.delenv("VERIFY_CLIENT_CERT", raising=False)
    importlib.reload(config)
    assert config.VERIFY_CLIENT_CERT is True


def test_verify_client_cert_false(monkeypatch):
    monkeypatch.setenv("VERIFY_CLIENT_CERT", "false")
    importlib.reload(config)
    assert config.VERIFY_CLIENT_CERT is False


def test_verify_client_cert_true_case_insensitive(monkeypatch):
    monkeypatch.setenv("VERIFY_CLIENT_CERT", "TRUE")
    importlib.reload(config)
    assert config.VERIFY_CLIENT_CERT is True
