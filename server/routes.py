import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

demo_bp = Blueprint("demo", __name__)


@demo_bp.route("/demo/current")
def current():
    now = datetime.now(timezone.utc)
    timestamp = str(int(now.timestamp() * 1000))
    logger.info("zonedDateTime: %s", now)
    logger.info("timestamp: %s", timestamp)
    return jsonify({"zonedDateTime": str(now), "timestamp": timestamp})
