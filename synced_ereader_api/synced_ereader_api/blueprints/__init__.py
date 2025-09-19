"""Blueprint collection.

Import and expose blueprints here for central registration in the app factory.
"""
from .api.routes import api_bp

__all__ = ["api_bp"]
