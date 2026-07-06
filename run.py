import logging
import os
import socket
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

from server import config, create_app

log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs(config.LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(),
        TimedRotatingFileHandler(
            filename=os.path.join(config.LOG_DIR, "app.log"),
            when="midnight",
            backupCount=30,
            encoding="utf-8",
        ),
    ],
)

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    from server.ssl_context import create_ssl_context

    protocol = config.SERVER_PROTOCOL

    if protocol == "http":
        logger.info("Starting HTTP server on %s:%s", config.SERVER_HOST, config.SERVER_PORT)
        from waitress import serve
        serve(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
    else:
        if protocol != "https":
            logger.warning("Unknown SERVER_PROTOCOL '%s', falling back to https", protocol)
        logger.info("Starting HTTPS server on %s:%s", config.SERVER_HOST, config.SERVER_PORT)
        ssl_ctx = create_ssl_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.SERVER_HOST, config.SERVER_PORT))
        sock.listen(5)
        ssl_sock = ssl_ctx.wrap_socket(sock, server_side=True)
        from waitress import serve
        serve(app, sockets=[ssl_sock])
