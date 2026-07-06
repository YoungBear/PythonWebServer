import os

ENV = "production"
DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CERT_DIR = os.path.join(BASE_DIR, "cert")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")
SERVER_KEY_PASSWORD = "ServerKey@2024"
ROOTCA_CERT = os.path.join(CERT_DIR, "rootca.crt")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8888"))

_context_path = os.getenv("CONTEXT_PATH", "/PythonWebServer")
CONTEXT_PATH = _context_path if _context_path.startswith("/") else "/" + _context_path
