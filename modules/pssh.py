from __future__ import annotations
from modules.logging import setup_logging
from modules.proxy import init_proxy, allowed_countries
from colorama import Fore, Style
from typing import Optional
from modules.utils import bypass_manifest_fetching
from modules.proxy import used_proxy
from requests.adapters import HTTPAdapter
import xml.etree.ElementTree as ET
import base64, os, requests, uuid, struct, m3u8, xmltodict, json, sys, re, time

logging = setup_logging()

def used_proxy(proxy):
    session = requests.Session()
    if proxy:
        if isinstance(proxy, dict):
            session.proxies.update(proxy)
        else:
            session.proxies.update({
                'http': "http://" + proxy,
                'https': "http://" + proxy
            })
    return session

def fetch_manifest(url, proxy):
    logging.info(f"{Fore.YELLOW}CONTENT: {Fore.RED}{url}{Fore.RESET}")
    print(Fore.MAGENTA + "=============================================================================================================\n")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
    session = used_proxy(proxy)
    
    try:
        response = session.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as http_err:
        if http_err.response.status_code == 403:
            logging.info(f"{Fore.YELLOW}Forbidden - {Fore.RED}[403]: {Fore.GREEN}Attempting to bypass manifest fetching..{Fore.RESET}")
            print(Fore.MAGENTA + "=" * 120 + "\n")
            return bypass_manifest_fetching(url)
        else:
            logging.error("Failed to retrieve PSSH data using bypass method.")
            return None
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

def extract_kid_and_pssh_from_mpd(manifest):
    if not isinstance(manifest, str):
        logging.error(f"Expected string or bytes-like object, got {type(manifest)}")
        return None, None

    kid_pattern = re.compile(r'<ContentProtection\s+.*?cenc:default_KID="([^"]+)".*?>', re.DOTALL)
    pssh_pattern = re.compile(r'<ContentProtection\s+.*?urn:uuid:(?:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed|EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED)".*?<cenc:pssh.*?>(.*?)</cenc:pssh>', re.DOTALL)
    
    kid_matches = kid_pattern.findall(manifest)
    pssh_matches = pssh_pattern.findall(manifest)

    if kid_matches:
        logging.info(f"{Fore.YELLOW}KID: {Fore.RED}{kid_matches[0]}{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120)
    else:
        logging.info("No KID found in manifest.")
    
    if pssh_matches:
        return pssh_matches[0]
    
    if not pssh_matches:
        logging.info(f"{Fore.YELLOW}PSSH NOT FOUND, {Fore.GREEN}GENERATING NEW PSSH...{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120)
        return kid_to_pssh(kid_matches)
        
    else:
        logging.info("No PSSH Data found in manifest.")
        return None

def kid_to_pssh(kid):
    url = "http://127.0.0.1:1337/dev/widevine/kid_to_pssh"
    data = {"kid": kid}
    response = requests.post(url, json=data)
    pssh = response.json()["responseData"]["pssh"]
    return pssh

def get_pssh(url: str, proxy=None) -> Optional[str]:
    try:
        # Fetch the manifest based on the URL type (MPD or M3U8)
        manifest = fetch_manifest(url, proxy)
        if not manifest:
            logging.error(f"Failed to fetch manifest from: {url}")
            return None

        # Handling .mpd file URLs
        if '.mpd' in url:
            pssh = extract_kid_and_pssh_from_mpd(manifest)
            if pssh:
                # Return PSSH in Base64 format after re-encoding
                pssh_encoded = base64.b64encode(base64.b64decode(pssh)).decode('utf-8')
                logging.info(f"Successfully extracted PSSH from MPD: {pssh_encoded[:50]}...")  # Log part of the encoded PSSH for verification
                return pssh_encoded
            else:
                logging.error("Failed to extract PSSH from MPD manifest.")
                return None

        # Handling .m3u8 file URLs
        elif '.m3u8' in url:
            m3u8_obj = fetch_m3u8(url)
            if not m3u8_obj:
                logging.error(f"Failed to fetch M3U8 from URL: {url}")
                return None
            pssh = extract_pssh_from_m3u8(m3u8_obj)
            if pssh:
                logging.info(f"Successfully extracted PSSH from M3U8: {pssh[:50]}...")  # Log part of the PSSH
                return pssh
            else:
                logging.error("Failed to extract PSSH from M3U8 manifest.")
                return None

        # If the manifest URL type is unsupported
        logging.error("Unsupported manifest type or failed extraction.")
        return None

    except Exception as e:
        logging.error(f"An error occurred while processing the PSSH extraction: {e}")
        return None

def get_pssh_from_mpd(manifest_url, proxy=None):
    pssh = ''
    try:
        r = requests.get(url=manifest_url, proxies=proxy)
        r.raise_for_status()
        xml = xmltodict.parse(r.text)
        mpd = json.loads(json.dumps(xml))
        periods = mpd.get('MPD', {}).get('Period', [])
    except Exception as e:
        logging.error(f"Error: Unable to fetch or parse MPD manifest: {e}")
        return input("Please enter PSSH manually: ")

    if not isinstance(periods, list):
        periods = [periods]

    try:
        for period in periods:
            adaptation_sets = period.get('AdaptationSet', [])
            if not isinstance(adaptation_sets, list):
                adaptation_sets = [adaptation_sets]
            
            for ad_set in adaptation_sets:
                if ad_set.get('@mimeType') == 'video/mp4':
                    content_protections = ad_set.get('ContentProtection', [])
                    if not isinstance(content_protections, list):
                        content_protections = [content_protections]
                    
                    for content_protection in content_protections:
                        if content_protection.get('@schemeIdUri', '').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                            pssh = content_protection.get("cenc:pssh", '')
                            if pssh:
                                break
                    if pssh:
                        break
            if pssh:
                break
    except Exception as e:
        logging.error(f"Error parsing MPD content: {e}")
    
    if not pssh:
        pssh = input("Unable to find PSSH in MPD. Please enter PSSH manually: ")
    return pssh


def pssh_parser(base64_pssh):
    try:
        hex_pssh = base64.b64decode(base64_pssh).hex()
        match = re.search(r'000000[0-9a-fA-F]{2}70737368.*', hex_pssh)

        if match:
            extracted_hex = match.group(0)
            base64_extracted_string = base64.b64encode(bytes.fromhex(extracted_hex)).decode()
            return base64_extracted_string
        else:
            return None, "PSSH pattern not found."

    except (ValueError, base64.binascii.Error):
        return None, "Invalid Base64 input."
    
def fetch_m3u8(url: str) -> m3u8.M3U8:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return m3u8.loads(response.text)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch m3u8 playlist: {e}")
        raise

def extract_pssh_from_m3u8(m3u8_obj: m3u8.M3U8) -> Optional[str]:
    keys = m3u8_obj.keys + m3u8_obj.session_keys
    for key in keys:
        if key and key.uri and key.uri.startswith('data:text/plain;base64,'):
            base64_data = key.uri.split(',')[1]
            try:
                pssh_data = base64.b64decode(base64_data)
                return base64.b64encode(pssh_data).decode('utf-8')
            except (base64.binascii.Error, ValueError) as e:
                logging.error(f"Failed to decode Base64 data: {e}")
                return None
    return None

def get_pssh_from_m3u8_url(url: str) -> Optional[str]:
    try:
        m3u8_obj = fetch_m3u8(url)
        pssh = extract_pssh_from_m3u8(m3u8_obj)
        if pssh:
            return pssh
        logging.error("Failed to extract PSSH from m3u8.")
        return None
    except Exception as e:
        logging.error(f"An error occurred while fetching PSSH from m3u8 URL: {e}")
        return None

def extract_kid_and_pssh(url: str, proxy=None):
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
    print(Fore.MAGENTA + "=============================================================================================================\n")
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