"""Routes for the site (HTML pages).

This keeps HTML page concerns separated from API JSON endpoints.
"""
from __future__ import annotations

from flask import Blueprint, current_app, render_template, jsonify

site_bp = Blueprint("site", __name__)


@site_bp.route("/")
def index():
    return jsonify({"BIG":"BOSS"})
