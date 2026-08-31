import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CERT_DIR = os.path.join(BASE_DIR, "cert")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")
SERVER_KEY_PASSWORD = os.getenv("SERVER_KEY_PASSWORD", "")
ROOTCA_CERT = os.path.join(CERT_DIR, "rootca.crt")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8888"))

_context_path = os.getenv("CONTEXT_PATH", "/PythonWebServer").strip("/")
CONTEXT_PATH = f"/{_context_path}" if _context_path else "/"

SERVER_PROTOCOL = os.getenv("SERVER_PROTOCOL", "https").lower()
VERIFY_CLIENT_CERT = os.getenv("VERIFY_CLIENT_CERT", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.path.join(BASE_DIR, "logs")
