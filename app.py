import ssl
import logging
from datetime import datetime, timezone

from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/SpringBoot2Demo/demo/current")
def current():
    now = datetime.now(timezone.utc)
    timestamp = str(int(now.timestamp() * 1000))
    logger.info("zonedDateTime: %s", now)
    logger.info("timestamp: %s", timestamp)
    return jsonify({"zonedDateTime": str(now), "timestamp": timestamp})


def create_ssl_context():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(
        certfile="cert/server.crt",
        keyfile="cert/server.key",
        password="ServerKey@2024",
    )
    ctx.load_verify_locations(cafile="cert/rootca.crt")
    ctx.verify_mode = ssl.CERT_REQUIRED
    return ctx


if __name__ == "__main__":
    ssl_ctx = create_ssl_context()
    app.run(host="0.0.0.0", port=8888, ssl_context=ssl_ctx, debug=False)
