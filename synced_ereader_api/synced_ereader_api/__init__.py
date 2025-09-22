import logging.config

from flask import Flask

# Legacy single-blueprint module (kept temporarily for reference). New code
# should use the structured blueprints under `synced_ereader_api.blueprints`.
from synced_ereader_api.blueprints import api_bp
from synced_ereader_api.logging import init_logging
from dotenv import load_dotenv
from flask_cors import CORS


def create_app(config_overrides=None):
    init_logging()  # should be configured before any access to app.logger
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("synced_ereader_api.defaults")
    app.config.from_prefixed_env()
    # Allow CORS from any origin. This is equivalent to the previous implicit
    # call but is made explicit for clarity. Note: When origins='*', you cannot
    # use credentials (cookies/Authorization with withCredentials in browsers).
    # If later you need credentials, replace origins='*' with a specific list
    # (e.g. ["http://localhost:5173", "https://your.app"]).
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=False,
    )

    if config_overrides is not None:
        app.config.from_mapping(config_overrides)

    app.register_blueprint(api_bp)

    return app
