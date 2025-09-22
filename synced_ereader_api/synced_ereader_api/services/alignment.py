import json
from .shared import validate_request_data

def coarsely_align_book_transcription(request_data:json):
    try:
        validate_request_data(request_data, ["pages"])
    except ValueError as e:
        raise e
    
    print(request_data)

