from flask import Flask

from . import config
from .routes import demo_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("server.config")
    app.register_blueprint(demo_bp, url_prefix=config.CONTEXT_PATH)
    return app
