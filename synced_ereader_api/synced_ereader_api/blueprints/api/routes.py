"""JSON API endpoints.

Demonstrates a health endpoint and a dummy transcription endpoint calling into
service-layer code.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from pathlib import Path

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.post("/create-project/<project_name>")
def createProject(project_name):
    p = Path(current_app.config["PROJECTS_DIRECTORY"])
    new_path = p.resolve() / project_name

    if new_path.exists():
        return jsonify({"error": "project name already exists."}), 400

    try:
        new_path.mkdir()
    except:
        return jsonify({"error": "error creating directory with project name."}), 400
    finally:
        return jsonify({"project_name": project_name}), 201

@api_bp.get("/get-project-names")
def getProjectNames():
    p = Path(current_app.config["PROJECTS_DIRECTORY"])

    directoryNames = []
    for directory in (item for item in p.iterdir() if item.is_dir()):
        directoryNames.append(directory.name)

    return jsonify({"project names": directoryNames}), 200
    