"""JSON API endpoints.

Demonstrates a health endpoint and a dummy transcription endpoint calling into
service-layer code.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from pathlib import Path
from synced_ereader_api.services import create_project, list_projects

api_bp = Blueprint("api", __name__, url_prefix="/api")

# this endpoint is for creating a directory that represents an audio book.
# The created directory will hold all of the data generated during the transcription / alignment
@api_bp.post("/create-project/<project_name>")
def createProject(project_name):
    try:
        created_project_name = create_project(Path(current_app.config["PROJECTS_DIRECTORY"]), project_name)
    except FileExistsError:
        return jsonify({"error": "project name already exists."}), 400
    except OSError as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"project_name": created_project_name}), 201


@api_bp.get("/project-names")
def getProjectNames():
    return jsonify({"project names": list_projects(Path(current_app.config["PROJECTS_DIRECTORY"]))}), 200