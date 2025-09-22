import json

def validate_request_data(request_data:json , required_fields:list[str]):
    # validate correct input fields were provided.
    if not request_data:
        raise ValueError("No data was provided in the request body.")

    missing = [field for field in required_fields if field not in request_data]

    if len(missing) > 0:
        raise ValueError("The following required fields are not in request body: " + ",".join(missing))