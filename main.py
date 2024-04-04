import os
import argparse
import requests
import pyfiglet
import base64
from colorama import init, Fore
from modules.cdm.cdm import Cdm
from modules.cdm.deviceconfig import device_android_generic
from base64 import b64encode
from modules.cdm.pssh import get_pssh
from modules.cdm.wvdecryptcustom import WvDecrypt
from modules.headers import headers, data
import coloredlogs

# Initialize colorama and coloredlogs
init(autoreset=True)
coloredlogs.install(level='DEBUG')

def print_title(title_text):
    """Prints formatted title text."""
    title = pyfiglet.figlet_format(title_text, font='slant')
    print(Fore.MAGENTA + title + Fore.RESET)

def generate_pssh(mpd_url):
    """Generates PSSH."""
    print("\nGenerating PSSH...")
    pssh = get_pssh(mpd_url)
    print(f'\nPSSH: {pssh}')
    return pssh

def get_license_keys(pssh, lic_url):
    """Gets license keys."""
    print("\nGetting license keys...")
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=None, device=device_android_generic)
    data["widevine2Challenge"] = base64.b64decode(wvdecrypt.get_challenge())
    print("Widevine Challenge:", data["widevine2Challenge"])
    widevine_license = requests.post(url=lic_url, data=data, headers=headers)
    print("License request sent to:", lic_url)
    print("License response:", widevine_license.content)
    license_b64 = b64encode(widevine_license.content)
    print("Base64 encoded license:", license_b64)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    print("Keys retrieved:", keyswvdecrypt)
    return Correct, keyswvdecrypt

def print_license_keys(keys):
    """Prints license keys."""
    print("\nPrinting license keys...")
    for key in keys:
        print(Fore.CYAN + f'--key {key}' + Fore.RESET)
    print(Fore.GREEN + "\nAll Done..." + Fore.RESET)

def parse_arguments():
    """Parses command-line arguments."""
    print("\nParsing command-line arguments...")
    parser = argparse.ArgumentParser(description='WKS-KEYS v3 - A tool to obtain Widevine keys from MPD URLs')
    parser.add_argument('-u', '--license-url', required=True, help='URL to request Widevine license')
    parser.add_argument('-m', '--mpd-url', required=False, help='URL of the Media Presentation Description (MPD)')
    parser.add_argument('-p', '--pssh', required=False, help='Protection System Specific Header (PSSH)')
    args = parser.parse_args()
    print("Parsed arguments:", args)
    return args

def clear_screen():
    """Clears the screen."""
    print("\nClearing the screen...")
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print_title('WKS-KEYS 2.0')
    print(f"RECODED BY: {Fore.YELLOW}ThatNotEasy{Fore.RESET}\n")

    args = parse_arguments()
    lic_url = args.license_url

    if args.pssh:
        pssh = args.pssh
        print("Using provided PSSH:", pssh)
    else:
        MDP_URL = args.mpd_url
        print("Using MPD URL:", MDP_URL)
        pssh = generate_pssh(MDP_URL)

    correct, keys = get_license_keys(pssh, lic_url)
    print_license_keys(keys)

if __name__ == "__main__":
    main()
