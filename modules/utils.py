import shutil, sys, os
from pathlib import Path
from typing import Optional
import pyfiglet
from colorama import Fore, Style
import importlib
from modules.logging import setup_logging
import requests
import random
import os
import uuid, secrets
from colorama import Fore
from http.cookiejar import MozillaCookieJar

logging = setup_logging()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_input(prompt, color):
    print(color + prompt + Style.RESET_ALL, end='')
    return input()

def get_binary_path(*names: str) -> Optional[Path]:
    """Get the path of the first found binary name."""
    for name in names:
        path = shutil.which(name)
        if path:
            return Path(path)
    return None

def print_title(title_text, proxy=None):
    title = pyfiglet.figlet_format(title_text, font='slant')
    if proxy:
        print(Fore.YELLOW + f"{title}Running with proxy settings: {proxy}" + Style.RESET_ALL)
    else:
        print(Fore.CYAN + f"{title}Running " + Style.RESET_ALL)

def print_license_keys(keys):
    for key in keys:
        logging.info(key)
    print(Fore.MAGENTA + "=============================================================================================================")
    logging.success("All Done...")

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logging.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)
        
def get_cookies_module(service_name):
    try:
        return importlib.import_module(f'cookies.{service_name}')
    except ImportError:
        logging.error(f"No module named '{service_name}' found in 'cookies' package")
        sys.exit(1)

metadata_endpoint = 'https://www.netflix.com/nq/website/memberapi/{}/metadata'
default_file_name = "$ftitle$.$year$.$fseason$$fepisode$.NF.WEBDL.$quality$p.$audios$.$acodec$.$vcodec$-dvx.mkv"

def random_hex(length: int) -> str:
	return "".join(random.choice("0123456789ABCDEF") for _ in range(length))

def pretty_size(size: int) -> str:
    return f"{size/float(1<<20):,.0f}MiB"


manifest_esn = f"NFCDIE-03-{random_hex(30)}"
def get_android_esn(quality: int) -> str:
    if quality >= 2160:
        device_id = 2  # 4K quality
    elif quality >= 1080:
        device_id = 1  # Full HD quality
    else:
        device_id = 0  # Standard quality
    return f"NFANDROID{device_id}-PRV-P-SAMSUSM-G950F-7169-{random_hex(30)}" # NFCDCH-02-L6JNYW0LWGPUCQVQ23JMWQW95UH1J1


def shakti_headers(build_id):
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'nfvdid=BQFmAAEBEO0P9Of-baB5Orb9r3fK8zJgR0INqZCZ-g-BpCVDkqpPtUcsPbZZb2Iakqn-RC0HCpKyS69LwkpsQf8LueRhO-YCxX4feGFexm9_SssxEo3wmysSRbhBd9CAwiJ1TWsMC0nkxuozO8hxIEjBecGFVA9X; flwssn=94e09c53-0493-4afb-8519-64ebe630480e; SecureNetflixId=v%3D3%26mac%3DAQEAEQABABRNGRQo9NNvDLWpGhQnmKFrKPtzg9zi4v4.%26dt%3D1720742390324; NetflixId=ct%3DBgjHlOvcAxLvAkMOL5MiJYYoxyB8ug0nHTitrlTEOFahRzzSvQhDR8xWrwSw7Rk5G1rxAWUA1t05x_6wumr2BdC4WfDruz2iG01l3n8OxL_ujD-BLc5bRUDv-FwotePryijVX4LLQmr_Tej0EBubkyqKGzVcVVgMqivRKlz_qCoeBcPg85Y-MfUQwkNjnVJ_RkZdI9OhgWftfLX8Na_hcxuW5hi27SUOozcdXIcVffm-BjiRZeYZfe_W2tGykdJx8PN_EzlUlyVsNCb33p5rlkBY6Ra7JAZy3slWsxpBCPMG5D2KKIV_41dmQSIDXAP9ziOPnMqawe2VS-CQ78FV1-vtCgX6WNDdgshhuCvf0dIvCoSzca_4fWTOX9XiZq-ElXLQXUMCjMBAemBHXTbNMcv6TZWl4ebEIHAvODzU_bTdMIwVbF9Kfgu2Mq9OstXoiy5wErqwcbnVaFjUIu0gajWgNxtOo53wDaPQbzq_vBqDl5G46Tp07tgYBiIOCgxlBJugchk05DEulWc.%26ch%3DAQEAEAABABTgnj9qpkN-KmSEQn85zAS3FX3lykQcOiw.%26v%3D3; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+12+2024+07%3A59%3A33+GMT%2B0800+(Malaysia+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=ad873cbc-84bb-4606-b4d6-f4aacefb3947&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; profilesNewSession=0',
        'dnt': '1',
        'origin': 'https://www.netflix.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-netflix.browsername': 'Chrome',
        'x-netflix.browserversion': '126',
        'x-netflix.client.request.name': 'ui/falcorUnclassified',
        'x-netflix.clienttype': 'akira',
        'x-netflix.esn': 'NFCDCH-02-L8Z2W1GRV6VKDKV3FP2EL9M6QVQYUT',
        'x-netflix.esnprefix': 'NFCDCH-02-',
        'x-netflix.nq.stack': 'prod',
        'x-netflix.osfullname': 'Windows 10',
        'x-netflix.osname': 'Windows',
        'x-netflix.osversion': '10.0',
        'x-netflix.request.client.user.guid': '7M7CH62HTNHJLHPSMAJAA5ZNU4',
        'x-netflix.uiversion': 'v1665dea6',
    }

def build_headers():
    return {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "en,en-US;q=0.9",
        "X-Forwarded-For": "194.36.178.234"
    }

def get_build_id() -> str:
    r = requests.get("https://www.netflix.com/buildIdentifier")
    if r.status_code != 200:
        print(f"{Fore.YELLOW}[Widevine-KSKEY] - {Fore.RED}Netflix didn't return 200!")
        raise Exception("Netflix didn't return 200")
    return r.json()["BUILD_IDENTIFIER"]

def read_data(cookies_file):
    if not os.path.exists(cookies_file):
        print(f"{Fore.YELLOW}[Widevine-KSKEY] - {Fore.RED}Missing cookie file. ({cookies_file})")
        raise Exception(f"Missing cookie file. ({cookies_file})")
    cj = MozillaCookieJar(cookies_file)
    cj.load()
    cookies = {
        cookie.name: cookie.value
        for cookie in cj
    }
    cookies["build_id"] = get_build_id()
    if "NetflixId" not in cookies:
        print(f"{Fore.YELLOW}[Widevine-KSKEY] - {Fore.RED}Invalid cookies. (Missing NetflixId)")
        raise Exception("Invalid cookies. (Missing NetflixId)")
    return cookies

lang_codes = {
    "fil": ["Filipino", "fil"],
    "cy": ["Welsh", "cym"],
    "cs": ["Czech", "ces"],
    "de": ["German", "ger"],
    "en": ["English", "eng"],
    "es": ["Spanish", "spa"],
    "bg": ["Bulgarian", "bul"],
    "ar-EG": ["Egyptian Arabic", "ara"],
    "ar-SY": ["Syrian Arabic", "ara"],
    "en-GB": ["Britain English", "eng"],
    "es-ES": ["European Spanish", "spa"],
    "fr-CA": ["Canadian French", "fra"],
    "fr": ["French", "fra"],
    "hi": ["Hindi", "hin"],
    "hu": ["Hungarian", "hun"],
    "id": ["Indonesian", "ind"], 
    "it": ["Italian", "ita"],
    "pl": ["Polish", "pol"],
    "pt-BR": ["Brazilian Portuguese", "por"],
    "ru": ["Russian", "rus"],
    "ta": ["Tamil", "tam"],
    "te": ["Telugu", "tel"],
    "th": ["Thai", "tha"],
    "tr": ["Turkish", "tur"],
    "uk": ["Ukrainian", "ukr"],
    "ar": ["Arabic", "ara"],
    "da": ["Danish", "dan"],
    "el": ["Greek", "ell"],
    "fi": ["Finnish", "fin"],
    "he": ["Hebrew", "heb"],
    "hi-Latn": ["Hindi", "hin"],
    "hr": ["Croatian", "hrv"],
    "ja": ["Japanese", "jpn"],
    "ko": ["Korean", "kor"],
    "ms": ["Malay", "msa"],
    "nb": ["Norwegian", "nob"],
    "nl": ["Dutch", "nld"],
    "pt": ["Portuguese", "por"],
    "ro": ["Romanian", "ron"],
    "sv": ["Swedish", "swe"],
    "vi": ["Vietnamese", "vie"],
    "zh": ["Chinese", "zho"],
    "zh-Hans": ["Simplified Chinese", "zho"],
    "zh-Hant": ["Traditional Chinese", "zho"]
}

supported_video_profiles = {
    "high": ["playready-h264hpl{}-dash"],
    "main": ["playready-h264mpl{}-dash"],
    "baseline": ["playready-h264bpl{}-dash"],
    "hevc": ["hevc-main10-L{}-dash-cenc", "hevc-main10-L{}-dash-cenc-prk"],
    "hdr": ["hevc-hdr-main10-L{}-dash-cenc", "hevc-hdr-main10-L{}-dash-cenc-prk"]
}

supported_audio_profiles = {
    "aac": [
        "heaac-5.1-dash",
        "heaac-5.1hq-dash",
        "heaac-2-dash",
        "heaac-2hq-dash",
    ],
    "ac3": [
        "dd-5.1-dash",
        "dd-5.1-elem"
    ],
    "eac3": [
        "ddplus-5.1-dash",
        "ddplus-5.1hq-dash",
        "ddplus-2-dash"
    ],
    "dts": [
        "ddplus-atmos-dash"
    ]
}

def get_profiles(video_profile: str, audio_profile: str, quality: int):
    profiles = ["webvtt-lssdh-ios8"]
    profile = supported_video_profiles.get(video_profile.lower())
    if quality >= 2160:
        profiles += list(map(lambda x: x.format(51), profile))
        profiles += list(map(lambda x: x.format(50), profile))
    if quality >= 1080:
        if video_profile.lower() in ["hevc", "hdr"]:
            profiles += list(map(lambda x: x.format(41), profile))
        profiles += list(map(lambda x: x.format(40), profile))
    if quality >= 720:
        profiles += list(map(lambda x: x.format(31), profile))
    if quality >= 480:
        profiles += list(map(lambda x: x.format(30), profile))
        if video_profile.lower not in ["hevc", "hdr"]:
            profiles += list(map(lambda x: x.format(22), profile))
    profiles += supported_audio_profiles.get(audio_profile.lower())
    return profiles
