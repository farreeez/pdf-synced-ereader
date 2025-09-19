"""JSON API endpoints.

Demonstrates a health endpoint and a dummy transcription endpoint calling into
service-layer code.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

