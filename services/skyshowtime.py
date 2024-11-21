import hmac, hashlib, sys, time, base64, requests, json
from modules.logging import setup_logging
from urllib.parse import urlparse

logging = setup_logging()

def get_headers():
    headers = {}
    return headers

def get_cookies():
    cookies = {}
    file_path = "cookies/skyshowtime.txt"
    logging.debug(f"Attempting to open cookie file at: {file_path}")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#') or not line.strip():
                    logging.debug("Skipping comment or empty line.")
                    continue
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    domain = parts[0]
                    flag = parts[1]
                    path = parts[2]
                    secure = parts[3]
                    expiration = parts[4]
                    name = parts[5]
                    value = parts[6]
                    cookies[name] = value
                    logging.debug(f"Added cookie: {name}={value} (Domain: {domain}, Path: {path})")

        logging.info(f"Successfully loaded {len(cookies)} cookies from {file_path}")

    except FileNotFoundError:
        logging.error(f"File not found: '{file_path}'")
    except Exception as e:
        logging.error(f"Error reading cookies from '{file_path}': {e}")

    return cookies


def calculate_signature(method, url, headers, payload, timestamp=None):
    app_id = 'SKYSHOWTIME-ANDROID-v1'
    signature_key = bytearray('jfj9qGg6aDHaBbFpH6wNEvN6cHuHtZVppHRvBgZs', 'utf-8')
    sig_version = '1.0'

    if not timestamp:
        timestamp = int(time.time())

    if url.startswith('http'):
        parsed_url = urlparse(url)
        path = parsed_url.path
    else:
        path = url

    text_headers = ''
    for key in sorted(headers.keys()):
        if key.lower().startswith('x-skyott'):
            text_headers += key + ': ' + headers[key] + '\n'
    headers_md5 = hashlib.md5(text_headers.encode()).hexdigest()

    if sys.version_info[0] > 2 and isinstance(payload, str):
        payload = payload.encode('utf-8')
    payload_md5 = hashlib.md5(payload).hexdigest()

    to_hash = ('{method}\n{path}\n{response_code}\n{app_id}\n{version}\n{headers_md5}\n'
               '{timestamp}\n{payload_md5}\n').format(method=method, path=path,
                                                      response_code='', app_id=app_id, version=sig_version,
                                                      headers_md5=headers_md5, timestamp=timestamp, payload_md5=payload_md5)

    hashed = hmac.new(signature_key, to_hash.encode('utf8'), hashlib.sha1).digest()
    signature = base64.b64encode(hashed).decode('utf8')
    return 'SkyOTT client="{}",signature="{}",timestamp="{}",version="{}"'.format(app_id, signature, timestamp, sig_version)

def get_user_token(token_url, cookies, region):
    headers = {
        'Accept': 'application/vnd.playvod.v1+json',
        'Content-Type': 'application/vnd.playvod.v1+json',
    }
    post_data = {
        "auth": {
            "authScheme": 'MESSO',
            "authIssuer": 'NOWTV',
            "provider": 'SKYSHOWTIME',
            "providerTerritory": region,
            "proposition": 'SKYSHOWTIME',
        },
        "device": {
            "type": 'MOBILE',
            "platform": 'ANDROID',
            "id": 'Z-sKxKApSe7c3dAMGAYtVU8NmWKDcWrCKobKpnVTLqc',
            "drmDeviceId": 'UNKNOWN'
        }
    }
    post_data = json.dumps(post_data)
    headers['x-sky-signature'] = calculate_signature('POST', token_url, headers, post_data)
    response = requests.post(token_url, cookies=cookies, headers=headers, data=post_data)
    response.raise_for_status()
    return response.json()['userToken']

def get_vod_request(vod_url, region, user_token, video_url):
    content_id = video_url.split("/")[6]
    provider_variant_id = video_url.split("/")[7][:36]
    post_data = {
        "providerVariantId": provider_variant_id,
        "device": {
            "capabilities": [
                {"transport": "DASH", "protection": "NONE", "vcodec": "H265", "acodec": "AAC", "container": "ISOBMFF"},
                {"transport": "DASH", "protection": "WIDEVINE", "vcodec": "H265", "acodec": "AAC", "container": "ISOBMFF"},
                {"transport": "DASH", "protection": "NONE", "vcodec": "H264", "acodec": "AAC", "container": "ISOBMFF"},
                {"transport": "DASH", "protection": "WIDEVINE", "vcodec": "H264", "acodec": "AAC", "container": "ISOBMFF"}
            ],
            "model": "SM-N986B",
            "maxVideoFormat": "HD",
            "hdcpEnabled": 'false',
            "supportedColourSpaces": ["SDR"]
        },
        "client": {"thirdParties": ["COMSCORE", "CONVIVA", "FREEWHEEL"]},
        "personaParentalControlRating": 9
    }
    post_data = json.dumps(post_data)
    headers = {
        'accept': 'application/vnd.playvod.v1+json',
        'content-type': 'application/vnd.playvod.v1+json',
        'x-skyott-activeterritory': region,
        'x-skyott-agent': 'skyshowtime.mobile.android',
        'x-skyott-country': region,
        'x-skyott-device': 'MOBILE',
        'x-skyott-platform': 'ANDROID',
        'x-skyott-proposition': 'SKYSHOWTIME',
        'x-skyott-provider': 'SKYSHOWTIME',
        'x-skyott-territory': region,
        'x-skyott-usertoken': user_token,
    }
    headers['x-sky-signature'] = calculate_signature('POST', vod_url, headers, post_data)
    response = requests.post(vod_url, headers=headers, data=post_data)
    response.raise_for_status()
    logging.info(response.json()['asset']['endpoints'][0]['url'])
    return response.json()