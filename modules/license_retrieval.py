import requests, glob, os, base64, json, urllib3, services.vdocipher
from base64 import b64encode, b64decode
from modules.utils import get_service_module, is_token_valid
from modules.proxy import used_proxy
from pywidevine.pssh import PSSH
from pywidevine.device import Device
from pywidevine.cdm import Cdm
from services.hbogo import get_license
from modules.pssh import get_pssh_from_mpd, kid_to_pssh
from services.skyshowtime import get_user_token, get_vod_request
from services import paralelo
from colorama import Fore
from modules.logging import setup_logging
from modules.config import load_configurations
from modules.proxy import used_proxy
from services.learnyst import ConfigManager, Learnyst, PlayerManager
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging = setup_logging()
config = load_configurations()
cf = ConfigManager()
cf.initialize()
    
    
def load_first_wvd_file(directory="device"):
    wvd_files = glob.glob(os.path.join(directory, '*.wvd'))
    if wvd_files:
        return Device.load(wvd_files[0])
    else:
        logging.error("No .wvd files found in the directory.")

def configure_session(proxy):
    session = requests.Session()
    if proxy:
        session.proxies.update(proxy)
    return session

def get_license_keys(pssh, lic_url, service_name, content_id=None, proxy=None, kid=None):
    logging.info(f"{Fore.YELLOW}SERVICE: {Fore.GREEN}{service_name}")
    print(Fore.MAGENTA + "=" * 120)
    logging.info(f"{Fore.YELLOW}PSSH: {Fore.RED}{pssh}")
    print(Fore.MAGENTA + "=" * 120)
    logging.info(f"{Fore.YELLOW}LICENSE: {Fore.RED}{lic_url}")
    print(Fore.MAGENTA + "=" * 120)
    # logging.info(f"{Fore.YELLOW}Proxies: {Fore.RED}{proxy}")
    # print(Fore.MAGENTA + "=" * 120)

    if service_name == "hbogo":
        if not content_id:
            logging.error("Content ID is required for HBOGO service.")
            return False, None
        data = get_license(content_id)
        logging.debug(f"License data: {data}")
        return True, []
    
    device = load_first_wvd_file()
    cdm = Cdm.from_device(device)
    session_id = cdm.open()
    challenge_bytes = cdm.get_license_challenge(session_id, PSSH(pssh))
    challenge_b64 = b64encode(challenge_bytes).decode('utf-8')
    
    service_module = get_service_module(service_name)
    headers = getattr(service_module, 'get_headers', lambda: {})()
    get_data_func = getattr(service_module, 'get_data', lambda: {})
    params = getattr(service_module, 'get_params', lambda: {})()
    cookies = getattr(service_module, 'get_cookies', lambda: {})()
    
    if service_name == "vdocipher" and challenge_b64:
        data = get_data_func(challenge_b64)
    else:
        data = get_data_func()

    if not pssh and kid:
        pssh = kid_to_pssh(kid)
        
    if service_module == "learnyst":
        print(service_module)
        
    
    try:
        proxies = used_proxy(proxy)
        session = requests.Session()
        if proxies:
            session.proxies.update(proxies if isinstance(proxy, dict) else {
                'http': proxy,
                'https': proxy
            })
        
        # Make the request
        if service_name == "prime":
            data['widevine2Challenge'] = challenge_b64
            response = session.post(url=lic_url, headers=headers, params=params, cookies=cookies, json=data, proxies=proxies)
        elif service_name in ["astro", "music-amz", "audible"]:
            data['licenseChallenge'] = challenge_b64
            response = session.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxies)
        elif service_name == "apple":
            data['streaming-request']['streaming-keys'][0]['challenge'] = challenge_b64
            response = session.post(url=lic_url, headers=headers, json=data, proxies=proxies)
        elif service_name in ["byutv", "moviestar", "ppv", "sooka","tonton", "roku", "toggo", "videoland"]:
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, proxies=proxies)
        elif service_name == "youku":
            data["licenseRequest"] = b64decode(challenge_bytes)
            response = session.post(url=lic_url, headers=headers, data=data, proxies=proxies)
        elif service_name == "newsnow":
            data["licenseRequest"] = challenge_b64
            response = session.post(url=lic_url, headers=headers, cookies=cookies, json=data, proxies=proxies)
        elif service_name in ["filmo", "viaplay", "peacock", "viki", "paramountplus", "crunchyroll", "hbomax"]:
            response = session.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=challenge_bytes, proxies=proxies)
        elif service_name in ["amcplus", "preladder", "ivi","dazn","unifi"]:
            response = session.post(url=lic_url, headers=headers, params=params, data=challenge_bytes, proxies=proxies)
        elif service_name == "rakuten":
            response = session.post(url=lic_url, headers=headers, params=params, data=challenge_bytes, proxies=proxies)
        elif service_name in ["jio","cignal"]:
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, proxies=proxies, verify=False)
        elif service_name == "starzon":
            decoded_bytes = base64.b64decode(challenge_b64)
            data["drm_info"] = list(decoded_bytes)
            response = session.post(url=lic_url, headers=headers, json=data, proxies=proxies)
        elif service_name in ["flow", "tvdmm"]:
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, cookies=cookies, proxies=proxies)
        elif service_name == "skyshowtime":
            token_url = 'https://ovp.skyshowtime.com/auth/tokens'
            vod_url = 'https://ovp.skyshowtime.com/video/playouts/vod'
            region = cookies.get('activeTerritory')
            user_token = get_user_token(token_url, cookies, region)
            video_url = content_id
            vod_request = get_vod_request(vod_url, region, user_token, video_url)
            license_url = vod_request.get('protection', {}).get('licenceAcquisitionUrl')
            manifest_url = vod_request.get('asset', {}).get('endpoints', [{}])[0].get('url')
            pssh = get_pssh_from_mpd(manifest_url)
            response = session.post(url=license_url, headers=headers, cookies=cookies, data=challenge_bytes, proxies=proxy)
        elif service_name in ["emocje", "virgintv","udemy"]:
            response = session.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=challenge_bytes, proxies=proxies)
        elif service_name in ["oneplus","tfc"]:
            response = session.post(url=lic_url, headers=headers, params=params, data=challenge_bytes, proxies=proxies)
        elif service_name == "directtv":
            data["licenseChallenge"] = challenge_b64
            response = session.post(url=lic_url, headers=headers, json=data, proxies=proxies)
        elif service_name == "canal":
            data["ServiceRequest"]["InData"]["ChallengeInfo"] = challenge_b64
            response = session.post(url=lic_url, headers=headers, json=data, proxies=proxies)
        elif service_name == "paralelo":
            data = paralelo.get_data().get('query')
            response = session.post(url=lic_url, headers=headers, json={'query': data}, proxies=proxies)
        elif service_name in ["tataplay", "channel5", "mtv"]:
            response = session.post(url=lic_url, headers=headers, params=params, data=challenge_bytes, proxies=proxies, verify=False)
            print(response.text)
        elif service_name in ["rugbytv", "ufc", "swaglive","vtmgo"]:
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, proxies=proxies)
            print(response.text)
        elif service_name == "videotron":
            data_dict = json.loads(data)
            json_data = json.dumps(data_dict)
            response = session.post(url=lic_url, headers=headers, data=json_data, proxies=proxies)
        elif service_name == "todtv":
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, proxies=proxies)
        elif service_name == "telia":
            data["Payload"] = challenge_b64
            data["LatensRegistration"]["DeviceInfo"]["DeviceType"] = "Android"
            json_string = json.dumps(data)
            modified_encoded_data = base64.b64encode(json_string.encode('utf-8'))
            modified_encoded_data_str = modified_encoded_data.decode('utf-8')
            response = session.post(url=lic_url, headers=headers, data=modified_encoded_data_str, proxies=proxies)
        elif service_name == "amateurtv":
            response = session.post(url=lic_url, headers=headers, cookies=cookies, data=challenge_bytes, proxies=proxies)
        elif service_name in ["exxen", "hotstar", "mewatch"]:
            response = session.post(url=lic_url, headers=headers, data=challenge_bytes, proxies=proxies)
        elif service_name in ["fubo","itv"]:
            response = session.post(url=lic_url, headers=headers, params=params, data=challenge_bytes, proxies=proxies)
        elif service_name == "vdocipher":
            vdo = services.vdocipher.get_data(challenge_b64)
            response = session.post(url=lic_url, headers=headers, json=vdo, proxies=proxies)
        elif service_name == "polsat":
            data["params"]["object"] = challenge_b64
            data = json.dumps(data)
            response = session.post(url=lic_url, headers=headers, data=data, proxies=proxies)
        elif service_name == "polsat":
            data["params"]["object"] = challenge_b64
            data = json.dumps(data)
            response = session.post(url=lic_url, headers=headers, data=data, proxies=proxies)
        else:
            response = session.post(url=lic_url, headers=headers, params=params, cookies=cookies, data=challenge_bytes, proxies=proxies)
    
        if response.status_code != 200:
            logging.error(f"Failed to retrieve license: {response.text}")
            return False, None

        if service_name == "prime":
            license_b64 = response.json()["widevine2License"]["license"]
        elif service_name == "astro":
            license_b64 = response.json()["licenseData"][0]
        elif service_name in ["skyshowtime","tonton", "bitmovin", "unifi", "rakuten", "paramountplus", "joyn", "beinsports", "viki", "hbomax"]:
            license_b64 = b64encode(response.content).decode()
        elif service_name == "apple":
            license_b64 = response.json()['streaming-response']['streaming-keys'][0]['license']
        elif service_name == "youku":
            response_data_bytes = b64decode(response.json()["data"].encode('utf-8'))
            license_b64 = b64encode(response_data_bytes).decode()
        elif service_name in ["sooka", "mubi", "dazn", "vdocipher", "newsnow", "beinsports", "viaplay", "peacock"]:
            license_b64 = b64encode(response.content).decode()
        elif service_name in ["music-amz", "crunchyroll", "videoland"]:
            license_b64 = response.json()["license"]
        elif service_name == "filmo":
            license_b64 = base64.b64encode(response.content)
        elif service_name == "udemy":
            license_b64 = b64encode(response.content).decode()
        elif service_name == "virgintv":
            license_b64 = response.content
        elif service_name == "directtv":
            license_b64 = response.json()['licenseData']
        elif service_name == "canal":
            license_b64 = response.json()["ServiceResponse"]["OutData"]["LicenseInfo"]
        elif service_name == "paralelo":
            license_b64 = response.json()["data"]["drm_license"]["license"]
        elif service_name in ["amcplus", "byutv", "moviestar", "emocje","fubo","ufc", "cignal","mtv","ivi","swaglive", "starzon", "roku", "tfc","exxen", "mewatch","todtv", "channel5", "hotstar", "amateurtv", "itv", "tvdmm"]:
            license_b64 = b64encode(response.content).decode()
        elif service_name in ["vtmgo", "videotron", "audible"]:
            license_b64 = response.json()["license"]
        elif service_name == "oneplus":
            license_b64 = response.json()["data"]
        elif service_name == "polsat":
            licenses = json.loads(response.text)
            license_b64 = licenses.get("result", {}).get("object", {}).get("license", None)
        else:
            logging.error(f"Service '{service_name}' is not handled.")
            return False, None

        cdm.parse_license(session_id, license_b64)
        returned_keys = []
        cached_keys = ""
        for key in cdm.get_keys(session_id):
            if key.type != "SIGNING":
                returned_keys.append(f"--key {key.kid.hex}:{key.key.hex()}")
                cached_keys += f"{Fore.YELLOW}--key {Fore.GREEN}{key.kid.hex}:{key.key.hex()}{Fore.RESET}\n"
        cdm.close(session_id)

        return returned_keys
    except requests.RequestException as e:
        logging.info(f"{Fore.YELLOW}Status: {Fore.RED}{e}{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120)
        
        
def handle_learnyst_service(manifest_url, lr_token=None):
    """
    Handle license retrieval for Learnyst service.
    """
    if not lr_token:
        lr_token = cf.simple_get("lrToken")
        if not lr_token:
            lr_token = input(f"{Fore.RED}[INFO]: {Fore.WHITE}lrToken/authToken not found, please re-enter: ")
            cf.simple_set("lrToken", lr_token)
    
    logging.info("Injecting exports into player...")
    player_manager = PlayerManager(token=lr_token, version=455, lc=50, player_file='player.js')
    
    if not player_manager.get_player():
        logging.error("Unable to request player")
        return False
    if not player_manager.inject_exports():
        logging.error("Unable to inject exports")
        return False

    logging.info("Verifying token...")
    if not is_token_valid(lr_token):
        logging.error("Token expired, please re-enter")
        cf.simple_set("lrToken", None)
        return False

    if not manifest_url:
        logging.error("Manifest URL not provided for Learnyst download.")
        return False

    logging.info(f"Starting Learnyst download with manifest URL: {manifest_url}")
    learnyst = Learnyst(url=manifest_url, token=lr_token)
    learnyst.download()
    return True

class REMOTE_CDM:
    def __init__(self, apikey):
        self.pssh = None
        self.license_b64 = None
        self.challenge_b64 = None
        self.session_id = None
        self.session = requests.Session()
        self.apikey = apikey
        
    def get_challenge(self, pssh):
        r = requests.post("https://dev.kepala-pantas.xyz/dev/playready/get_challenge", json={"pssh": pssh}, headers={"X-API-KEY": self.apikey})
        challenge_b64 = r.json()["responseData"]["challenge_b64"]
        session_id = r.json()["responseData"]["session_id"]
        return challenge_b64, session_id

    def get_keys(self, license_b64, session_id):
        r = requests.post("https://dev.kepala-pantas.xyz/dev/playready/get_keys", json={"license_b64": license_b64, "session_id": session_id}, headers={"X-API-KEY": self.apikey})
        keys = r.json()["responseData"]["keys"]
        return keys