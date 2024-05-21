import os, sys, argparse, requests, importlib, pyfiglet, ssl, json, coloredlogs
from base64 import b64encode, b64decode
from colorama import init
from modules.pssh import get_pssh, PSSH
from modules.device import Device
from modules.cdm import Cdm
from services.hbogo import get_license
from loguru import logger
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ciphers="HIGH:!DH:!aNULL"
        )

# Initialize colorama and coloredlogs
init(autoreset=True)
session = requests.Session()
coloredlogs.install(level='DEBUG')
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", level="DEBUG")

def parse_arguments():
    parser = argparse.ArgumentParser(description='WKS-KEYS 2.0 - A tool to obtain Widevine keys from MPD URLs')
    parser.add_argument('-u', '--license-url', required=False, help='URL to request Widevine license')
    parser.add_argument('-m', '--mpd-url', help='URL of the Media Presentation Description (MPD)')
    parser.add_argument('-pp', '--proxy', help='Specify the proxy to use for the requests')
    parser.add_argument('-p', '--pssh', required=False, help='Protection System Specific Header (PSSH)')
    parser.add_argument('-s', '--service', required=True, help='Specify the service module (e.g., prime, netflix)')
    parser.add_argument('-c', '--content-id', required=False, help='Specify the content id for HBOGO modules')
    return parser.parse_args()

def generate_pssh(mpd_url):
    return get_pssh(mpd_url)

def print_title(title_text, proxy=None):
    title = pyfiglet.figlet_format(title_text, font='slant')
    logger.debug(title)
    if proxy:
        logger.debug(f"Proxy: {proxy}")

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logger.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)

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
    
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Data: {data}")
    logger.debug(f"Params: {params}")
    logger.debug(f"Cookies: {cookies}")

    device = Device.load('modules/devices/google_sdk_gphone64_x86_64_16.1.0_1275dddb_22596_l3.wvd')
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

def print_license_keys(keys):
    for key in keys:
        logger.info(key)
    logger.success("All Done...")

def main():
    args = parse_arguments()
    print_title('\n' + 'Widevine-KSKEY', args.proxy)
    
    lic_url = args.license_url
    pssh = args.pssh or (generate_pssh(args.mpd_url) if args.mpd_url else None)

    if not pssh and args.service != "hbogo":
        logger.error("No PSSH data provided or extracted.")
        return
    
    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    
    keys = get_license_keys(pssh, lic_url, args.service, args.content_id, proxy)
    if keys:
        print_license_keys(keys)
    else:
        logger.error("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()
