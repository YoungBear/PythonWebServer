from flask import Flask, jsonify
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

from . import config
from .routes import demo_bp

_swagger_config = {
    "title": "PythonWebServer API",
    "version": "1.0.0",
    "openapi": "3.0.3",
    "specs_route": "/apidocs/",
    "specs": [{"endpoint": "apispec_1", "route": "/apispec_1.json"}],
    "headers": [],
}

_swagger_template = {
    "info": {
        "title": "PythonWebServer API",
        "description": "Flask HTTPS Web Server with mTLS — 对应 SpringBoot2Demo 的 Python 实现",
        "version": "1.0.0",
    },
    "servers": [{"url": f"{config.SERVER_PROTOCOL}://localhost:{config.SERVER_PORT}"}],
}


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("server.config")
    app.register_blueprint(demo_bp, url_prefix=config.CONTEXT_PATH)

    Swagger(app, config=_swagger_config, template=_swagger_template)

    register_error_handlers(app)
    register_health(app)

    return app


def register_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.name, "status": e.code}), e.code

    @app.errorhandler(Exception)
    def handle_unhandled(e):
        app.logger.exception("Unhandled exception: %s", e)
        return jsonify({"error": "Internal Server Error", "status": 500}), 500


def register_health(app: Flask):
    from datetime import datetime, timezone

    @app.route("/health")
    def health():
        """
        Health Check
        ---
        tags:
          - System
        summary: 健康检查
        description: 返回服务运行状态，始终在根路径，不受 CONTEXT_PATH 影响。
        responses:
          200:
            description: 服务正常
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    status:
                      type: string
                      example: "UP"
                    timestamp:
                      type: string
                      example: "1783321215118"
        """
        return jsonify({
            "status": "UP",
            "timestamp": str(int(datetime.now(timezone.utc).timestamp() * 1000)),
        })
