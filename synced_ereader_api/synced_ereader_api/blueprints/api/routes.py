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

# Expects a boolean value in the body that shows wether the expected audio book is in multiple files or in a single file.
# If it is a single audio file then the URI provided should be the URI to the singular audio file if the boolean is true or to the directory
# containing all of the audio files for the audiobooks if it is false 
@api_bp.post("/transcribe-audiobook")
def transcribeAudioBook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data was provided in the request body."}), 400

    required_fields = ["path", "is_single_audio_file"]

    missing = [field for field in required_fields if field not in data]

    if len(missing) > 0:
        return jsonify({"error": "The following required fields are not in request body: " + ",".join(missing)}), 400

    # if is single audio is true check that URI is for a file otherwise check that it is for a directory.

    isSingleFile = data["is_single_audio_file"]

    if type(isSingleFile) is not bool:
        return jsonify({"error": "The field is_single_audio_file must be a boolean."}), 400
    
    rawAudioPath = data["path"]

    audioPath = Path(rawAudioPath)

    if not (audioPath.is_absolute() and audioPath.exists()):
        return jsonify({"error": "URI provided is invalid."}), 400

    if isSingleFile and audioPath.is_dir():
        return jsonify({"error": "is_single_file is set to true, but the path provided is for a folder."}), 400

    if (not isSingleFile) and audioPath.is_file():
        return jsonify({"error": "is_single_file is set to false, but the path provided is for a file."}), 400

    return jsonify({"good":"no problems with request body"}), 200

