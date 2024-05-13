import xml.etree.ElementTree as ET
import base64
import requests
import uuid
import struct

import requests, xmltodict, json

def get_pssh(mpd_url):
    pssh = ''
    try:
        r = requests.get(url=mpd_url)
        r.raise_for_status()
        xml = xmltodict.parse(r.text)
        mpd = json.loads(json.dumps(xml))
        periods = mpd['MPD']['Period']
    except Exception as e:
        pssh = input(f'\nUnable to find PSSH in MPD: {e}. \nEdit getPSSH.py or enter PSSH manually: ')
        return pssh
    try: 
        if isinstance(periods, list):
            for idx, period in enumerate(periods):
                if isinstance(period['AdaptationSet'], list):
                    for ad_set in period['AdaptationSet']:
                        if ad_set['@mimeType'] == 'video/mp4':
                            try:
                                for t in ad_set['ContentProtection']:
                                    if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                        pssh = t["cenc:pssh"]
                            except Exception:
                                pass   
                else:
                    if period['AdaptationSet']['@mimeType'] == 'video/mp4':
                            try:
                                for t in period['AdaptationSet']['ContentProtection']:
                                    if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                        pssh = t["cenc:pssh"]
                            except Exception:
                                pass   
        else:
            for ad_set in periods['AdaptationSet']:
                    if ad_set['@mimeType'] == 'video/mp4':
                        try:
                            for t in ad_set['ContentProtection']:
                                if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                    pssh = t["cenc:pssh"]
                        except Exception:
                            pass   
    except Exception:
        pass                      
    if pssh == '':
        pssh = input('Unable to find PSSH in mpd. Edit getPSSH.py or enter PSSH manually: ')
    return pssh

def fetch_mpd_content(url):
    """Fetch MPD content from a URL."""
    response = requests.get(url)
    response.raise_for_status()  # Will raise an exception for HTTP errors
    return response.text

def extract_widevine_pssh_base64_from_mpd(mpd_content):
    """
    Extract Widevine PSSH data from MPD (DASH Manifest) content in Base64 format.

    Args:
    mpd_content (str): MPD file content as a string.

    Returns:
    list of dict: List containing dicts with keys 'schemeIdUri' and 'pssh' (Base64 encoded) specific to Widevine.
    """
    root = ET.fromstring(mpd_content)
    widevine_pssh_data_list = []
    widevine_scheme_id = "urn:uuid:EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED"

    for content_protection in root.iter('{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
        if content_protection.attrib.get('schemeIdUri') == widevine_scheme_id:
            cenc_pssh = content_protection.find('{urn:mpeg:cenc:2013}pssh')
            if cenc_pssh is not None:
                pssh_base64 = cenc_pssh.text.strip()
                widevine_pssh_data_list.append({
                    'schemeIdUri': widevine_scheme_id,
                    'pssh': pssh_base64
                })

    return widevine_pssh_data_list

def base64_to_pssh_box_base64(base64_pssh, system_id):
    try:
        pssh_data = base64.b64decode(base64_pssh)
    except base64.binascii.Error as e:
        return None, f"Base64 decoding error: {e}"
    
    system_id_bytes = uuid.UUID(system_id).bytes
    box_size = 32 + len(pssh_data)
    pssh_box = struct.pack('>I4s', box_size, b'pssh')
    pssh_box += struct.pack('>I', 0)
    pssh_box += system_id_bytes
    pssh_box += struct.pack('>I', len(pssh_data))
    pssh_box += pssh_data
    pssh_box_base64 = base64.b64encode(pssh_box).decode('utf-8')

    return pssh_box_base64, None

def process_mpd(mpd_url, system_id):
    mpd_content = fetch_mpd_content(mpd_url)
    widevine_pssh_data_base64 = extract_widevine_pssh_base64_from_mpd(mpd_content)

    if widevine_pssh_data_base64:
        base64_pssh = widevine_pssh_data_base64[0]['pssh']
        pssh_box_base64, error = base64_to_pssh_box_base64(base64_pssh, system_id)
        if pssh_box_base64:
            return pssh_box_base64, None
        else:
            return None, f"Failed to convert PSSH data: {error}"
    else:
        return None, "No Widevine PSSH data found in the MPD."