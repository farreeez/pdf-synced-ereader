"""Blueprint collection.

Import and expose blueprints here for central registration in the app factory.
"""
from .site.routes import site_bp
from .api.routes import api_bp

__all__ = ["site_bp", "api_bp"]
