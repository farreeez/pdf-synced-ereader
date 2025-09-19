import logging.config

from flask import Flask

# Legacy single-blueprint module (kept temporarily for reference). New code
# should use the structured blueprints under `synced_ereader_api.blueprints`.
from synced_ereader_api.blueprints import site_bp, api_bp
from synced_ereader_api.logging import init_logging


def create_app(config_overrides=None):
    init_logging()  # should be configured before any access to app.logger

    app = Flask(__name__)
    app.config.from_object("synced_ereader_api.defaults")
    app.config.from_prefixed_env()

    if config_overrides is not None:
        app.config.from_mapping(config_overrides)

    app.register_blueprint(site_bp)
    app.register_blueprint(api_bp)

    return app
