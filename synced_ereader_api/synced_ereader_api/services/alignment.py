import json
from .shared import validate_request_data

def coarsely_align_book_transcription(request_data:json):
    try:
        validate_request_data(request_data, ["pages"])
    except ValueError as e:
        raise e
    
    if not isinstance(request_data["pages"], list) or not all(isinstance(item, str) for item in request_data["pages"]):
        raise ValueError("request data provided is not a list of string.")
