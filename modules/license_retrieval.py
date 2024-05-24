import sys, requests, glob, os
from base64 import b64encode, b64decode
from loguru import logger
from modules.utils import get_service_module
from modules.pssh import PSSH
from modules.device import Device
from modules.cdm import Cdm
from services.hbogo import get_license
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def load_first_wvd_file(directory="."):
    wvd_files = glob.glob(os.path.join(directory, '*.wvd'))
    if wvd_files:
        return Device.load(wvd_files[0])
    else:
        raise FileNotFoundError("No .wvd files found in the directory.")

def get_license_keys(pssh, lic_url, service_name, content_id=None, proxy=None):
    logger.debug(f"Getting license keys for service: {service_name}")
    logger.debug(f"PSSH: {pssh}")
    logger.debug(f"License URL: {lic_url}")

    if service_name == "hbogo":
        if not content_id:
            logger.error("Content ID is required for HBOGO service.")
            return False, None
        data = get_license(content_id)
        logger.debug(f"License data: {data}")
        return True, []  # HBOGO license retrieval does not require other steps, so we return an empty list of keys

    service_module = get_service_module(service_name)
    
    headers = getattr(service_module, 'get_headers', lambda: {})()
    data = getattr(service_module, 'get_data', lambda: {})()
    params = getattr(service_module, 'get_params', lambda: {})()
    cookies = getattr(service_module, 'get_cookies', lambda: {})()
    
    # logger.debug(f"Headers: {headers}")
    # logger.debug(f"Data: {data}")
    # logger.debug(f"Params: {params}")
    # logger.debug(f"Cookies: {cookies}")

    device = load_first_wvd_file()
    cdm = Cdm.from_device(device)
    session_id = cdm.open()
    challenge = cdm.get_license_challenge(session_id, PSSH(pssh))
    challenge_b64 = b64encode(challenge).decode()
    
    if not pssh:
        logger.error("No PSSH data provided or extracted.")
        return False, None

    if service_name == "prime":
        data['widevine2Challenge'] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=data, proxies=proxy)
    elif service_name in ["astro", "apple"]:
        data['licenseChallenge'] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, json=data, proxies=proxy)
    elif service_name == "tonton":
        response = requests.post(url=lic_url, headers=headers, data=challenge, proxies=proxy)
    elif service_name == "youku":
        data["licenseRequest"] = b64decode(challenge)
        response = requests.post(url=lic_url, headers=headers, data=data, proxies=proxy)
    elif service_name in ["vdocipher", "newsnow"]:
        data["licenseRequest"] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxy, verify=False)
    elif service_name == "viaplay":
        response = requests.post(url=lic_url, headers=headers, data=challenge, proxies=proxy)
    elif service_name == "peacock":
        response = requests.post(url=lic_url, headers=headers, params=params, data=challenge_b64, proxies=proxy)
    elif service_name == "rakuten":
        response = requests.post(url=lic_url, headers=headers, data=challenge, proxies=proxy)
    elif service_name == "amazon":
        data['licenseChallenge'] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxy)
    else:
        response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=challenge, proxies=proxy)
    

    if response.status_code != 200:
        logger.error(f"Failed to retrieve license: {response.text}")
        return False, None

    if service_name == "prime":
        license_b64 = response.json()["widevine2License"]["license"]
    elif service_name == "astro":
        license_b64 = response.json()["licenseData"][0]
    elif service_name in ["tonton", "bitmovin", "unifi", "rakuten", "paramountplus", "joyn", "beinsports"]:
        license_b64 = b64encode(response.content).decode()
    elif service_name == "apple":
        license_b64 = response.json()['streaming-response']['streaming-keys'][0]['license']
    elif service_name == "youku":
        response_data_bytes = b64decode(response.json()["data"].encode('utf-8'))
        license_b64 = b64encode(response_data_bytes).decode()
    elif service_name == "mubi":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "dazn":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "vdocipher":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "newsnow":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "beinsports":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "viaplay":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "peacock":
        license_b64 = b64encode(response.content).decode()
    elif service_name == "amazon":
        license_b64 = response.json()["license"]
    else:
        logger.error(f"Service '{service_name}' is not handled.")
        return False, None

    cdm.parse_license(session_id, license_b64)
    returned_keys = []
    cached_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            returned_keys.append(f"--key {key.kid.hex}:{key.key.hex()}")
            cached_keys += f"{key.kid.hex}:{key.key.hex()}\n"
    cdm.close(session_id)
    return returned_keys