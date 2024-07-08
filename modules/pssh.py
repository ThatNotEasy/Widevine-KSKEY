from __future__ import annotations
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import base64
import requests
import uuid
import struct
import m3u8
import requests, xmltodict, json
import binascii, sys
import string, re, time
from io import BytesIO
from typing import Optional, Union
from uuid import UUID
from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET
from modules.logging import setup_logging
import construct
from construct import Container
from pymp4.parser import Box
from urllib.parse import urlparse, parse_qs
from modules.proxy import init_proxy, allowed_countries
from colorama import Fore, Style

logging = setup_logging()


def fetch_manifest(url, proxy=None):
    logging.info(f"{Fore.YELLOW}Fetching manifest from URL: {Fore.RED}{url}{Fore.RESET}")
    print(Fore.MAGENTA + "=============================================================================================================")
    response = requests.get(url, proxies=proxy)
    response.raise_for_status()
    return response.text

def extract_kid_and_pssh_from_mpd(manifest):
    try:
        # Define regex patterns to find the default_KID and PSSH data within the ContentProtection elements
        kid_pattern = re.compile(
            r'<ContentProtection\s+schemeIdUri="urn:mpeg:dash:mp4protection:2011".*?cenc:default_KID="(.*?)"',
            re.DOTALL
        )
        pssh_pattern = re.compile(
            r'<ContentProtection\s+schemeIdUri="urn:uuid:(?:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed|EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED)".*?<cenc:pssh.*?>(.*?)</cenc:pssh>',
            re.DOTALL
        )
        
        kid_matches = kid_pattern.findall(manifest)
        pssh_matches = pssh_pattern.findall(manifest)

        if kid_matches and pssh_matches:
            # Returning the first KID and PSSH pair for simplicity
            return kid_matches[0], pssh_matches[0]

        logging.warning("No KID or PSSH data found in MPD manifest.")
        return None, None
    except Exception as e:
        logging.error(f"Error extracting KID and PSSH from MPD manifest: {e}")
        raise

def get_pssh(url, proxy=None):
    try:
        kid, pssh = extract_kid_and_pssh(url, proxy)
        if not pssh:
            logging.error("No PSSH data provided or extracted.")
            return None
        logging.info(f"{Fore.YELLOW}KID: {Fore.RED}{kid}")
        print(Fore.MAGENTA + "=============================================================================================================")
        pssh_encoded = base64.b64encode(base64.b64decode(pssh)).decode('utf-8')
        
        if not pssh_encoded:
            logging.error("PSSH encoding failed.")
            return None
        return pssh_encoded
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

def get_pssh_from_mpd(mpd_url, proxy=None):
    pssh = ''
    try:
        r = requests.get(url=mpd_url, proxies=proxy)
        r.raise_for_status()
        xml = xmltodict.parse(r.text)
        mpd = json.loads(json.dumps(xml))
        periods = mpd.get('MPD', {}).get('Period', [])
    except Exception as e:
        pssh = input(f'\nUnable to find PSSH in MPD: {e}. \nEdit getPSSH.py or enter PSSH manually: ')
        return pssh

    try:
        if isinstance(periods, list):
            for period in periods:
                if isinstance(period.get('AdaptationSet', []), list):
                    for ad_set in period['AdaptationSet']:
                        if ad_set.get('@mimeType') == 'video/mp4':
                            try:
                                for t in ad_set.get('ContentProtection', []):
                                    if t.get('@schemeIdUri', '').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                        pssh = t.get("cenc:pssh", '')
                            except Exception:
                                pass
                else:
                    ad_set = period.get('AdaptationSet', {})
                    if ad_set.get('@mimeType') == 'video/mp4':
                        try:
                            for t in ad_set.get('ContentProtection', []):
                                if t.get('@schemeIdUri', '').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                    pssh = t.get("cenc:pssh", '')
                        except Exception:
                            pass
        else:
            ad_set = periods.get('AdaptationSet', {})
            if ad_set.get('@mimeType') == 'video/mp4':
                try:
                    for t in ad_set.get('ContentProtection', []):
                        if t.get('@schemeIdUri', '').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                            pssh = t.get("cenc:pssh", '')
                except Exception:
                    pass
    except Exception:
        pass
    
    if pssh == '':
        pssh = input('Unable to find PSSH in MPD. Edit getPSSH.py or enter PSSH manually: ')
    return pssh

def fetch_m3u8(url: str) -> m3u8.M3U8:
    response = requests.get(url)
    response.raise_for_status()
    return m3u8.loads(response.text)

def extract_pssh_from_m3u8(m3u8_obj: m3u8.M3U8) -> str:
    keys = m3u8_obj.keys + m3u8_obj.session_keys
    for key in keys:
        if key and key.uri and key.uri.startswith('data:text/plain;base64,'):
            base64_data = key.uri.split(',')[1]
            pssh_data = base64.b64decode(base64_data)
            return base64.b64encode(pssh_data).decode('utf-8')
    return None

def extract_kid_and_pssh(url, proxy=None):
    manifest = fetch_manifest(url, proxy)
    if '.mpd' in url:
        return extract_kid_and_pssh_from_mpd(manifest)
    elif '.m3u8' in url:
        m3u8_obj = fetch_m3u8(url)
        pssh = extract_pssh_from_m3u8(m3u8_obj)
        if pssh:
            return None, pssh
        else:
            logging.warning("PSSH extraction from m3u8 manifests failed.")
            return None, None
    else:
        raise ValueError(f"Unsupported manifest type for URL: {url}")

def fetch_manifest_with_retry(url, proxy=None, retries=3, backoff_factor=2):
    for i in range(retries):
        try:
            response = requests.get(url, proxies=proxy)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logging.error(f"429 Too Many Requests. Retry {i + 1}/{retries}. Waiting {backoff_factor ** i} seconds.")
                time.sleep(backoff_factor ** i)
                if i == retries - 1:
                    country_code = input("Proxy? (2 letter country code or N for no): ").strip().upper()
                    if len(country_code) == 2 and country_code in allowed_countries:
                        proxy = {"http": init_proxy({"zone": country_code, "port": "peer"})}
                        # print(f"Using proxy {proxy['http']}")
                    elif country_code == 'N':
                        proxy = None
                    else:
                        print(f"{Fore.RED}Invalid country code.{Style.RESET_ALL}")
                        sys.exit(1)
            else:
                raise e
    raise Exception(f"Failed to fetch manifest after {retries} retries due to too many requests (429).")


def amz_pssh(url, proxy=None):
    logging.info(f"{Fore.YELLOW}Fetching manifest from URL: {Fore.RED}{url}{Fore.RESET}")
    print(Fore.MAGENTA + "=============================================================================================================")
    system_id = "edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"
    response = requests.get(url, proxies=proxy)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    widevine_scheme_id = "urn:uuid:EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED"

    for content_protection in root.iter('{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
        if content_protection.attrib.get('schemeIdUri') == widevine_scheme_id:
            cenc_pssh = content_protection.find('{urn:mpeg:cenc:2013}pssh')
            if cenc_pssh is not None:
                pssh_base64 = cenc_pssh.text.strip()
                try:
                    pssh_data = base64.b64decode(pssh_base64)
                except base64.binascii.Error as e:
                    print("Base64 decoding error:", e)
                    return None

                system_id_bytes = uuid.UUID(system_id).bytes
                box_size = 32 + len(pssh_data)
                pssh_box = struct.pack('>I4s', box_size, b'pssh')
                pssh_box += struct.pack('>I', 0)
                pssh_box += system_id_bytes
                pssh_box += struct.pack('>I', len(pssh_data))
                pssh_box += pssh_data
                pssh_box_base64 = base64.b64encode(pssh_box).decode('utf-8')
                return pssh_box_base64
    return None