import os
import sys
import argparse
import requests
import importlib
import pyfiglet
from base64 import b64encode, b64decode
from colorama import init
from modules.deviceconfig import device_android_generic
from modules.pssh import get_pssh
from modules.wvdecryptcustom import WvDecrypt
from services.hbogo import get_license
from loguru import logger
import coloredlogs, os

# Initialize colorama and coloredlogs
init(autoreset=True)
coloredlogs.install(level='DEBUG')

# Configure loguru
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
    pssh = get_pssh(mpd_url)
    return pssh

def print_title(title_text):
    title = pyfiglet.figlet_format(title_text, font='slant')
    logger.debug(title)

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logger.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)

def get_license_keys(pssh, lic_url, service_module, content_id=None, proxy=None):
    if service_module == "hbogo":
        if not content_id:
            logger.error("Content ID is required for HBOGO service.")
            return False, None
        data = get_license(content_id)
        logger.debug(data)  # This line is just for testing purposes. You can remove it.
        return True, []  # HBOGO license retrieval does not require other steps, so we return an empty list of keys
    else:
        service = get_service_module(service_module)
        headers = getattr(service, 'get_headers', lambda: {})()
        data = getattr(service, 'get_data', lambda: {})()
        params = getattr(service, 'get_params', lambda: {})()
        cookies = getattr(service, 'get_cookies', lambda: {})()

        wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=None, device=device_android_generic)
        challenge = wvdecrypt.get_challenge()

        if not pssh:
            logger.error("No PSSH data provided or extracted.")
            return False, None

        if service_module == "prime":
            data['widevine2Challenge'] = b64encode(challenge).decode()
            response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=data)
            license_b64 = response.json()["widevine2License"]["license"]
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys

        elif service_module == "astro":
            data['licenseChallenge'] = b64encode(challenge).decode()
            response = requests.post(url=lic_url, headers=headers, json=data)
            license_b64 = response.json()["licenseData"][0]
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "tonton":
            response = requests.post(url=lic_url, params=params, headers=headers, data=challenge)
            license_b64 = b64encode(response.content)
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "apple":
            data['streaming-request']['streaming-keys'][0]['challenge'] = b64encode(challenge).decode()
            pssh = data['streaming-request']['streaming-keys'][0]['uri'].replace('data:text/plain;base64,', '')
            logger.debug("PSSH Data: {}", pssh)
            response = requests.post(url=lic_url, headers=headers, json=data)
            license_b64 = response.json()['streaming-response']['streaming-keys'][0]['license']
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "bitmovin":
            response = requests.post(url=lic_url, headers=headers, data=challenge)
            license_b64 = b64encode(response.content)
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "unifi":
            response = requests.post(url=lic_url, params=params, headers=headers, data=challenge)
            license_b64 = b64encode(response.content)
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "rakuten":
            response = requests.post(url=lic_url, params=params, headers=headers, data=challenge)
            license_b64 = b64encode(response.content)
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
        
        elif service_module == "paramountplus":
            response = requests.post(url=lic_url, params=params, headers=headers, data=challenge)
            license_b64 = b64encode(response.content)
            wvdecrypt.update_license(license_b64)
            Correct, keys = wvdecrypt.start_process()
            return Correct, keys
            
            

def print_license_keys(keys):
    for key in keys:
        logger.info(f'--key {key}')
    logger.success("\nAll Done...")


def main():
    print_title('\nWidevine-KSKEY')
    args = parse_arguments()
    lic_url = args.license_url

    pssh = args.pssh if args.pssh else generate_pssh(args.mpd_url) if args.mpd_url else None
    if not pssh and args.service != "hbogo":
        logger.error("No PSSH data provided or extracted.")
        return

    correct, keys = get_license_keys(pssh, lic_url, args.service, args.content_id, args.proxy)
    if correct:
        print_license_keys(keys)
    else:
        logger.error("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()
