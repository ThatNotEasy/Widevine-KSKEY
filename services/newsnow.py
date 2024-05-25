import urllib.parse

def get_cookies():
    cookies = {}
    return cookies

def get_headers():
    headers = {}
    return headers

def get_data():
    data = ''
    parsed_data = urllib.parse.parse_qs(data)
    data_dict = {key: value[0] for key, value in parsed_data.items()}
    return data_dict
