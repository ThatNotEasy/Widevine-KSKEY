import os
import sys
import argparse
import requests
import importlib
import pyfiglet
from base64 import b64encode
from colorama import init, Fore
from modules.deviceconfig import device_android_generic
from modules.pssh import get_pssh
from modules.wvdecryptcustom import WvDecrypt
import coloredlogs
from test import json_data

# Initialize colorama and coloredlogs
init(autoreset=True)
coloredlogs.install(level='DEBUG')

def generate_pssh(mpd_url):
    pssh = get_pssh(mpd_url)
    return pssh

def print_title(title_text):
    title = pyfiglet.figlet_format(title_text, font='slant')
    print(Fore.MAGENTA + title + Fore.RESET)

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        print(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)

def get_license_keys(pssh, lic_url, service_module):
    service = get_service_module(service_module)
    headers = service.get_headers()
    data = service.get_data()

    # Conditional handling of params and cookies based on the existence of these methods in the service module
    params = getattr(service, 'get_params', lambda: {})()  # Returns {} if get_params is not available
    cookies = getattr(service, 'get_cookies', lambda: {})()  # Returns {} if get_cookies is not available

    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=None, device=device_android_generic)
    challenge = wvdecrypt.get_challenge()

    if service_module == "prime":
        data['widevine2Challenge'] = b64encode(challenge).decode()
        response = requests.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=data)
        license_b64 = response.json()["widevine2License"]["license"]
        wvdecrypt.update_license(license_b64)
        Correct, keys = wvdecrypt.start_process()
        return Correct, keys

    elif service_module == "astro":
        json_data['licenseChallenge'] = b64encode(challenge).decode()
        response = requests.post(url=lic_url, headers=headers, json=json_data)
        license_b64 = response.json()["licenseData"][0]
        wvdecrypt.update_license(license_b64)
        Correct, keys = wvdecrypt.start_process()
        return Correct, keys

def print_license_keys(keys):
    for key in keys:
        print(Fore.CYAN + f'--key {key}' + Fore.RESET)
    print(Fore.GREEN + "\nAll Done..." + Fore.RESET)

def parse_arguments():
    parser = argparse.ArgumentParser(description='WKS-KEYS 2.0 - A tool to obtain Widevine keys from MPD URLs')
    parser.add_argument('-u', '--license-url', required=True, help='URL to request Widevine license')
    parser.add_argument('-m', '--mpd-url', help='URL of the Media Presentation Description (MPD)')
    parser.add_argument('-p', '--pssh', required=False, help='Protection System Specific Header (PSSH)')
    parser.add_argument('-s', '--service', required=True, help='Specify the service module (e.g., prime, netflix)')
    return parser.parse_args()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print_title('WKS-KEYS 2.0')
    args = parse_arguments()
    lic_url = args.license_url

    pssh = args.pssh if args.pssh else generate_pssh(args.mpd_url) if args.mpd_url else None
    
    if not pssh:
        print("No PSSH data provided or extracted.")
        return

    correct, keys = get_license_keys(pssh, lic_url, args.service)
    if correct:
        print_license_keys(keys)
    else:
        print("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()
