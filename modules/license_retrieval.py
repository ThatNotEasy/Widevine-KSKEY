import sys, requests, glob, os
from base64 import b64encode, b64decode
from modules.utils import get_service_module
from pywidevine.pssh import PSSH
from pywidevine.device import Device
from pywidevine.cdm import Cdm
from services.hbogo import get_license
from modules.pssh import get_pssh
from services.skyshowtime import get_user_token, get_vod_request, calculate_signature
from modules.initialization import initialize
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session, logging = initialize()

def load_first_wvd_file(directory="."):
    wvd_files = glob.glob(os.path.join(directory, '*.wvd'))
    if wvd_files:
        return Device.load(wvd_files[0])
    else:
        logging.error("No .wvd files found in the directory.")

def get_license_keys(pssh, lic_url, service_name, content_id=None, proxy=None):
    logging.info(f"Getting license keys for service: {service_name}")
    logging.info(f"PSSH: {pssh}")
    logging.info(f"License URL: {lic_url}")

    if service_name == "hbogo":
        if not content_id:
            logging.error("Content ID is required for HBOGO service.")
            return False, None
        data = get_license(content_id)
        logging.debug(f"License data: {data}")
        return True, []

    service_module = get_service_module(service_name)
    
    headers = getattr(service_module, 'get_headers', lambda: {})()
    data = getattr(service_module, 'get_data', lambda: {})()
    params = getattr(service_module, 'get_params', lambda: {})()
    cookies = getattr(service_module, 'get_cookies', lambda: {})()
    
    # logging.debug(f"Headers: {headers}")
    # logging.debug(f"Data: {data}")
    # logging.debug(f"Params: {params}")
    # logging.debug(f"Cookies: {cookies}")

    device = load_first_wvd_file()
    cdm = Cdm.from_device(device)
    session_id = cdm.open()
    challenge = cdm.get_license_challenge(session_id, PSSH(pssh))
    challenge_b64 = b64encode(challenge).decode('utf-8')
    
    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        return False, None

    if service_name == "prime":
        data['widevine2Challenge'] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, json=data, proxies=proxy)
    elif service_name in ["astro", "apple", "amazon"]:
        data['licenseChallenge'] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxy)
    elif service_name =="tonton":
        response = requests.post(url=lic_url, headers=headers ,data=challenge, proxies=proxy)
    elif service_name == "youku":
        data["licenseRequest"] = b64decode(challenge)
        response = requests.post(url=lic_url, headers=headers, data=data, proxies=proxy)
    elif service_name in ["vdocipher", "newsnow"]:
        data["licenseRequest"] = challenge_b64
        response = requests.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxy)
    elif service_name in ["viaplay", "peacock", "rakuten", "viki", "paramountplus", "crunchyroll"]:
        response = requests.post(url=lic_url, headers=headers, params=params, data=challenge, proxies=proxy)
    elif service_name == "unifi":
        response = requests.post(url=lic_url, headers=headers, params=params, data=challenge, proxies=proxy, verify=False)
    elif service_name == "skyshowtime":
        token_url = 'https://ovp.skyshowtime.com/auth/tokens'
        vod_url = 'https://ovp.skyshowtime.com/video/playouts/vod'
        region = cookies['activeTerritory']
        user_token = get_user_token(token_url, cookies, region)
        video_url = content_id
        vod_request = get_vod_request(vod_url, region, user_token, video_url)
        license_url = vod_request['protection']['licenceAcquisitionUrl']
        manifest_url = vod_request['asset']['endpoints'][0]['url']
        pssh = get_pssh(manifest_url)
        response = requests.post(url=license_url, headers=headers, data=challenge, proxies=proxy)
    else:
        response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=challenge, proxies=proxy)
    

    if response.status_code != 200:
        logging.error(f"Failed to retrieve license: {response.text}")
        return False, None

    if service_name == "prime":
        license_b64 = response.json()["widevine2License"]["license"]
    elif service_name == "astro":
        license_b64 = response.json()["licenseData"][0]
    elif service_name in ["skyshowtime","tonton", "bitmovin", "unifi", "rakuten", "paramountplus", "joyn", "beinsports", "viki"]:
        license_b64 = b64encode(response.content).decode()
    elif service_name == "apple":
        license_b64 = response.json()['streaming-response']['streaming-keys'][0]['license']
    elif service_name == "youku":
        response_data_bytes = b64decode(response.json()["data"].encode('utf-8'))
        license_b64 = b64encode(response_data_bytes).decode()
    elif service_name in ["mubi", "dazn", "vdocipher", "newsnow", "beinsports", "viaplay", "peacock"]:
        license_b64 = b64encode(response.content).decode()
    elif service_name in ["amazon", "crunchyroll"]:
        license_b64 = response.json()["license"]
    else:
        logging.error(f"Service '{service_name}' is not handled.")
        return False, None

    cdm.parse_license(session_id, license_b64)
    returned_keys = []
    cached_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            returned_keys.append(f"--key {key.kid.hex}:{key.key.hex()}")
            cached_keys += f"--key {key.kid.hex}:{key.key.hex()}\n"
    cdm.close(session_id)

    # output_file = "logs/keys.txt"
    # with open(output_file, "w") as file:
    #     file.write(cached_keys)

    # logging.info(f"Keys saved to {output_file}")
    return returned_keys