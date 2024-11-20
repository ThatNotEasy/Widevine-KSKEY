import requests
import uuid
import json
import random, os
from colorama import Fore
from modules.logging import setup_logging

logging = setup_logging()

ROTATE_PROXY = "https://dev.kepala-pantas.xyz/dev/osint/rotate-proxy"

class Settings:
    def __init__(self, userCountry: str = None, randomProxy: bool = False) -> None:
        self.randomProxy = randomProxy
        self.userCountry = userCountry
        self.ccgi_url = "https://client.hola.org/client_cgi/"
        self.ext_ver = self.get_ext_ver()
        self.ext_browser = "chrome"
        self.user_uuid = uuid.uuid4().hex
        self.user_agent = "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        self.product = "cws"
        self.port_type_choice: str
        self.zoneAvailable = [  # Comprehensive list of country codes
            "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AR", "AT", "AU", "AW", "AZ", "BA", "BB", "BD", "BE", "BF",
            "BG", "BH", "BI", "BJ", "BM", "BN", "BO", "BR", "BS", "BT", "BW", "BY", "BZ", "CA", "CD", "CF", "CG", "CH",
            "CI", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
            "EG", "ER", "ES", "ET", "FI", "FJ", "FM", "FR", "GA", "GB", "GD", "GE", "GH", "GM", "GN", "GQ", "GR", "GT",
            "GW", "GY", "HK", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IN", "IQ", "IR", "IS", "IT", "JM", "JO", "JP",
            "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT",
            "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MG", "MH", "MK", "ML", "MM", "MN", "MR", "MT", "MU", "MV", "MW",
            "MX", "MY", "MZ", "NA", "NE", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PG", "PH",
            "PK", "PL", "PT", "PW", "PY", "QA", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SI", "SK",
            "SL", "SM", "SN", "SO", "SR", "ST", "SV", "SY", "SZ", "TD", "TG", "TH", "TJ", "TL", "TM", "TN", "TO", "TR",
            "TT", "TV", "TZ", "UA", "UG", "US", "UY", "UZ", "VA", "VC", "VE", "VN", "VU", "WS", "YE", "ZA", "ZM", "ZW"
        ]

    def get_ext_ver(self) -> str:
        try:
            about = requests.get("https://hola.org/access/my/settings#/about").text
            if 'window.pub_config.init({"ver":"' in about:
                version = about.split('window.pub_config.init({"ver":"')[1].split('"')[0]
                logging.debug(f"Retrieved extension version: {version}")
                return version
        except requests.RequestException as e:
            logging.error(f"Request error while getting extension version: {e}")
        return "1.199.485"  # last known working version

class Engine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_proxy(self, tunnels, tls=False): 
        protocol = "https" if tls else "http"
        try:
            login_credentials = f"user-uuid-{self.settings.user_uuid}"
            for ip_address, port_details in tunnels["ip_list"].items():
                proxy_url = f"{protocol}://{login_credentials}:{tunnels['agent_key']}@{ip_address}:{port_details}"
                logging.debug(f"Generated proxy URL: {proxy_url}")
                return used_proxy(proxy_url)  # Use used_proxy here
        except KeyError as e:
            logging.error(f"Key missing when generating proxy URL: {e}")
            raise

    def generate_session_key(self, timeout: float = 10.0) -> str:
        post_data = {"login": "1", "ver": self.settings.ext_ver}
        try:
            response = requests.post(
                f"{self.settings.ccgi_url}background_init?uuid={self.settings.user_uuid}",
                json=post_data,
                headers={"User-Agent": self.settings.user_agent},
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()
            if "key" in data:
                logging.debug(f"Session key generated: {data['key']}")
                return data["key"]
            else:
                logging.error("Key not found in response: %s", data)
                raise KeyError("key")
        except requests.RequestException as e:
            logging.error(f"Request error while generating session key: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            raise
        except KeyError as e:
            logging.error(f"Key error: {e}")
            raise

    def zgettunnels(self, session_key: str, country: str, timeout: float = 10.0) -> dict:
        qs = {
            "country": country.lower(),
            "limit": 1,
            "ping_id": random.random(),
            "ext_ver": self.settings.ext_ver,
            "browser": self.settings.ext_browser,
            "uuid": self.settings.user_uuid,
            "session_key": session_key,
        }
        try:
            response = requests.post(
                f"{self.settings.ccgi_url}zgettunnels", params=qs, timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            logging.debug(f"Tunnels retrieved: {data}")
            return data
        except requests.RequestException as e:
            logging.error(f"Request error while getting tunnels: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            raise

class Hola:
    def __init__(self, settings: Settings) -> None:
        self.myipUri: str = "https://hola.org/myip.json"
        self.settings = settings

    def get_country(self) -> str:
        try:
            if not self.settings.randomProxy and not self.settings.userCountry:
                self.settings.userCountry = requests.get(self.myipUri).json()["country"]
                logging.debug(f"Retrieved user country: {self.settings.userCountry}")

            if (
                not self.settings.userCountry in self.settings.zoneAvailable
                or self.settings.randomProxy
            ):
                self.settings.userCountry = random.choice(self.settings.zoneAvailable)
                logging.debug(f"Randomly selected country: {self.settings.userCountry}")

            return self.settings.userCountry
        except requests.RequestException as e:
            logging.error(f"Request error while getting country: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            raise

def proxyscrape(country=None):
    PROXY_SCRAPE_URL = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies"
    if country:
        PROXY_SCRAPE_URL += f"&country={country}"
    PROXY_SCRAPE_URL += "&proxy_format=protocolipport&format=text"

    try:
        response = requests.get(PROXY_SCRAPE_URL)
        response.raise_for_status()
        proxies = response.text.split('\n')
        proxies = [proxy.strip() for proxy in proxies if proxy.strip()]

        # Normalize proxy format
        filtered_proxies = []
        for proxy in proxies:
            if proxy.startswith("socks"):
                filtered_proxies.append(proxy)
            else:
                if not proxy.startswith("http"):
                    proxy = "http://" + proxy
                filtered_proxies.append(proxy)

        if filtered_proxies:
            chosen_proxy = random.choice(filtered_proxies)
            logging.info(f"{Fore.YELLOW}Fetched {Fore.GREEN}{len(filtered_proxies)} {Fore.YELLOW}proxies from ProxyScrape. Selected proxy: {Fore.GREEN}{chosen_proxy}")
            print(Fore.MAGENTA + "=" * 120)
            return chosen_proxy
        else:
            logging.warning("No valid proxies found.")
            return None

    except requests.RequestException as e:
        logging.error(f"Request error while fetching proxies: {e}")
        return None

def init_proxy(data):
    settings = Settings(
        data["zone"]
    )  # True if you want random proxy each request / "DE" for a proxy with region of your choice (German here) / False if you wish to have a proxy localized to your IP address
    settings.port_type_choice = data[
        "port"
    ]  # direct return datacenter ipinfo, peer "residential" (can fail sometime)

    hola = Hola(settings)
    engine = Engine(settings)

    userCountry = hola.get_country()
    session_key = engine.generate_session_key()
    tunnels = engine.zgettunnels(session_key, userCountry)
    return engine.get_proxy(tunnels)

def rotate_proxy():
    try:
        response = requests.get(ROTATE_PROXY)
        response.raise_for_status()
        data = response.json()
        # Select the first available HTTP proxy and format correctly
        for proxy in data['proxies']:
            if proxy['protocol'].lower() == 'http':
                return {"http": f"http://{proxy['ipPort']}", "https": f"http://{proxy['ipPort']}"}
        raise ValueError("No suitable proxy found")
    except requests.RequestException as e:
        logging.error(f"Error fetching proxies: {e}")
        raise

allowed_countries = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AR", "AT", "AU", "AW", "AZ", "BA", "BB", "BD", "BE", "BF",
    "BG", "BH", "BI", "BJ", "BM", "BN", "BO", "BR", "BS", "BT", "BW", "BY", "BZ", "CA", "CD", "CF", "CG", "CH",
    "CI", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
    "EG", "ER", "ES", "ET", "FI", "FJ", "FM", "FR", "GA", "GB", "GD", "GE", "GH", "GM", "GN", "GQ", "GR", "GT",
    "GW", "GY", "HK", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IN", "IQ", "IR", "IS", "IT", "JM", "JO", "JP",
    "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT",
    "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MG", "MH", "MK", "ML", "MM", "MN", "MR", "MT", "MU", "MV", "MW",
    "MX", "MY", "MZ", "NA", "NE", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PG", "PH",
    "PK", "PL", "PT", "PW", "PY", "QA", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SI", "SK",
    "SL", "SM", "SN", "SO", "SR", "ST", "SV", "SY", "SZ", "TD", "TG", "TH", "TJ", "TL", "TM", "TN", "TO", "TR",
    "TT", "TV", "TZ", "UA", "UG", "US", "UY", "UZ", "VA", "VC", "VE", "VN", "VU", "WS", "YE", "ZA", "ZM", "ZW"
]

def create_default_proxies(filename):
    # Define default proxies, adjust as needed
    default_proxies = [
        'http://101.255.118.89:8080',
        'http://198.51.100.100:3128'
    ]
    
    # Create the file and write the default proxies if the file does not exist or is empty
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w') as file:
            for proxy in default_proxies:
                file.write(proxy + '\n')
        print(f"File {filename} created with default proxies.")

def read_proxies_from_file(filename):
    proxies = []
    create_default_proxies(filename)
    try:
        with open(filename, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return proxies


def used_proxy(proxy):
    if isinstance(proxy, dict):
        return proxy  # Assumes dictionary is properly formatted
    elif isinstance(proxy, str):
        return {'http': proxy, 'https': proxy}
    return {}

def configure_session(proxy):
    session = requests.Session()
    if proxy:
        session.proxies.update(proxy)
    return session

def get_tunnel_and_setup_proxy(session_key, country):
    tunnels = Engine.zgettunnels(session_key, country)
    if tunnels:
        proxy_url = Engine.get_proxy(tunnels)
        if proxy_url:
            working_proxies = used_proxy(proxy_url)
            session = configure_session(working_proxies)
            return session
    return None