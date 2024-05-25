import base64, xmltodict, json, requests, struct, uuid
import xml.etree.ElementTree as ET

def find_pssh_in_mpd(mpd_url):
    """
    Fetches an MPD file from a URL and extracts PSSH data from it.
    """
    response = requests.get(mpd_url)
    response.raise_for_status()  # This ensures we raise an error for bad HTTP status codes
    mpd_dict = xmltodict.parse(response.text)
    mpd_json = json.loads(json.dumps(mpd_dict))

    # Ensure 'Period' is a list
    periods = mpd_json['MPD']['Period']
    if not isinstance(periods, list):
        periods = [periods]  # Convert to list if not already a list

    pssh_data = []

    for period in periods:
        adaptation_sets = period['AdaptationSet']
        if not isinstance(adaptation_sets, list):
            adaptation_sets = [adaptation_sets]  # Convert to list if not already a list

        for adaptation_set in adaptation_sets:
            content_protections = adaptation_set.get('ContentProtection', [])
            if not isinstance(content_protections, list):
                content_protections = [content_protections]  # Convert to list if there's only one

            for cp in content_protections:
                if cp.get('@schemeIdUri', '').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed" and 'cenc:pssh' in cp:
                    pssh_data.append(cp['cenc:pssh'])

    return pssh_data

def get_default_kid_and_pssh(mpd_url):
    """
    Extracts the default KID and PSSH from an MPD file. Generates a PSSH box if no PSSH is found.
    """
    pssh = ''
    default_kid = None
    error = None

    try:
        response = requests.get(mpd_url)
        response.raise_for_status()
        mpd_dict = xmltodict.parse(response.text)
        mpd_json = json.loads(json.dumps(mpd_dict))
        periods = mpd_json['MPD']['Period']

        # Attempt to find default KID and PSSH
        if isinstance(periods, list):
            for period in periods:
                if isinstance(period['AdaptationSet'], list):
                    for ad_set in period['AdaptationSet']:
                        for content_protection in ad_set.get('ContentProtection', []):
                            if '@default_KID' in content_protection:
                                default_kid = content_protection['@default_KID'].replace('-', '')
                            if 'cenc:pssh' in content_protection and '@schemeIdUri' in content_protection:
                                if content_protection['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                    pssh = content_protection['cenc:pssh']
                                    break
                if pssh:
                    break
    except Exception as e:
        error = f"Error fetching or parsing MPD: {e}"
        return None, None, error

    if not pssh and default_kid:
        # Generate PSSH box if no PSSH is found but a default KID is available
        pssh = generate_pssh_with_default_kid("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed", default_kid)
        error = 'Generated PSSH using default KID due to absence in MPD.'

    return pssh, default_kid, error

def generate_pssh_with_default_kid(system_id, default_kid):
    """
    Generate a Widevine PSSH box using the system ID and a default KID.
    """
    system_id_bytes = uuid.UUID(system_id).bytes
    kid_bytes = uuid.UUID(default_kid).bytes

    # Widevine PSSH box format includes:
    box_size = 32 + 16  # Box size: header (32 bytes) + KID size (16 bytes)
    pssh_box = struct.pack('>I4sI', box_size, b'pssh', 0)  # Box header
    pssh_box += system_id_bytes  # System ID
    pssh_box += struct.pack('>I16s', 1, kid_bytes)  # KID count and KID

    return base64.b64encode(pssh_box).decode('utf-8')

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
    widevine_scheme_id = "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"

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