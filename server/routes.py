import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

demo_bp = Blueprint("demo", __name__)


@demo_bp.route("/demo/current")
def current():
    """
    Current Time
    ---
    tags:
      - Demo
    summary: 获取当前 UTC 时间
    description: 返回当前 UTC 时间的 zonedDateTime 字符串和时间戳（毫秒）。
    responses:
      200:
        description: 成功返回当前时间
        content:
          application/json:
            schema:
              type: object
              properties:
                zonedDateTime:
                  type: string
                  example: "2026-07-06 07:00:15.118021+00:00"
                timestamp:
                  type: string
                  example: "1783321215118"
    """
    now = datetime.now(timezone.utc)
    timestamp = str(int(now.timestamp() * 1000))
    logger.info("zonedDateTime: %s", now)
    logger.info("timestamp: %s", timestamp)
    return jsonify({"zonedDateTime": str(now), "timestamp": timestamp})
