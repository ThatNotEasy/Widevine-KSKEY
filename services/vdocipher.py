import json, base64

def get_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://player.vdocipher.com',
        'priority': 'u=1, i',
        'referer': 'https://player.vdocipher.com/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'vdo-sdk': 'VdoWeb/2.4.29',
    }
    return headers

def get_data():
    data = {
        "videoId": "d2792024231012043b9a80432954cd4e",
        "jwt": "ChBDeUhpcEFOcG9NS0ZqV2JLEhDSeSAkIxASBDuagEMpVM1OOJrknbIGQhcSFQgCEhF3d3cudmRvY2lwaGVyLmNvbQ.ZSh_fmVQeo4bmr_umB0M6BvVNybccUXCVMPcDqt5veo",
        "href": "https://www.vdocipher.com/",
        "tech": "wv",
        "licenseRequest": None
    }
    json_string = json.dumps(data)
    encoded_json = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')  # Encode as bytes before base64 encoding
    encoded_data = {"token": encoded_json}
    return encoded_data