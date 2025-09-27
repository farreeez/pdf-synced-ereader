"""JSON API endpoints.

Demonstrates a health endpoint and a dummy transcription endpoint calling into
service-layer code.
"""
from __future__ import annotations

from flask import Blueprint, jsonify, request, current_app
from pathlib import Path
from synced_ereader_api.services import create_project, list_projects, transcribe_audio, coarsely_align_book_transcription

api_bp = Blueprint("api", __name__, url_prefix="/api")

# this endpoint is for creating a directory that represents an audio book.
# The created directory will hold all of the data generated during the transcription / alignment
@api_bp.post("/create-project/<project_name>")
def createProject(project_name):
    Path(current_app.config["PROJECTS_DIRECTORY"]).mkdir(exist_ok=True)

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

# Expects a boolean value in the body that shows wether the expected audio book is in multiple files or in a single file.
# If it is a single audio file then the URI provided should be the URI to the singular audio file if the boolean is true or to the directory
# containing all of the audio files for the audiobooks if it is false 
@api_bp.post("/transcribe-audiobook/<project_name>")
def transcribeAudioBook(project_name):
    base_dir = Path(current_app.config["PROJECTS_DIRECTORY"])

    project_path = (base_dir / project_name).resolve()

    if not project_path.exists():
        return jsonify({"error":"Project name does not exist."}), 400

    data = request.get_json()

    try:
        transcribe_audio(data, project_path)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return '',201

@api_bp.post("/coarse-alignment/<project_name>")
def coarselyAlignTranscriptToPdf(project_name):
    base_dir = Path(current_app.config["PROJECTS_DIRECTORY"])

    project_path = (base_dir / project_name).resolve()

    if not project_path.exists():
        return jsonify({"error":"Project name does not exist."}), 400
    
    coarsely_align_book_transcription(request.get_json())

    return '',201
