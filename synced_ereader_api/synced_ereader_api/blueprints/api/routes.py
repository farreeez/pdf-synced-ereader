"""JSON API endpoints.

Demonstrates a health endpoint and a dummy transcription endpoint calling into
service-layer code.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.post("/create-project/<project_name>")
def createProject(project_name):
    return jsonify({"project_name": project_name}), 201

