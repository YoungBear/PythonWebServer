import os
import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from server import config, create_app

app = create_app()

if __name__ == "__main__":
    from server.ssl_context import create_ssl_context

    protocol = os.getenv("SERVER_PROTOCOL", "https").lower()
    if protocol == "http":
        app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=False)
    else:
        if protocol != "https":
            logger.warning("Unknown SERVER_PROTOCOL '%s', falling back to https", protocol)
        ssl_ctx = create_ssl_context()
        app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, ssl_context=ssl_ctx, debug=False)
