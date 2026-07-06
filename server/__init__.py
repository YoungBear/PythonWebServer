from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from . import config
from .routes import demo_bp
from .swagger import swagger_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("server.config")
    app.register_blueprint(demo_bp, url_prefix=config.CONTEXT_PATH)
    app.register_blueprint(swagger_bp)

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
        return jsonify({
            "status": "UP",
            "timestamp": str(int(datetime.now(timezone.utc).timestamp() * 1000)),
        })
