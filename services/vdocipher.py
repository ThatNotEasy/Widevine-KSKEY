import json, base64

def get_headers():
    headers = {}
    return headers

def get_data():
    data = {}
    json_string = json.dumps(data)
    encoded_json = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')  # Encode as bytes before base64 encoding
    encoded_data = {"token": encoded_json}
    return encoded_data