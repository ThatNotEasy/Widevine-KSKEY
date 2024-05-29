import httpx, uuid, json, random

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
        self.zoneAvailable = ["AR", "AT", "AU", "BE", "BG", "BR", "CA", "CH", "CL", "CO", "CZ", "DE", "DK", "ES", "FI",
                              "FR", "GR", "HK", "HR", "HU", "ID", "IE", "IL", "IN", "IS", "IT", "JP", "KR", "MX", "NL",
                              "NO", "NZ", "PL", "RO", "RU", "SE", "SG", "SK", "TR", "UK", "US", "GB"]

    def get_ext_ver(self) -> str:
        about = httpx.get("https://hola.org/access/my/settings#/about").text
        if 'window.pub_config.init({"ver":"' in about:
            version = about.split('window.pub_config.init({"ver":"')[1].split('"')[0]
            return version

        # last know working version
        return "1.199.485"


class Engine:
    def __init__(self, Settings) -> None:
        self.settings = Settings

    def get_proxy(self, tunnels, tls=False) -> str:
        login = f"user-uuid-{self.settings.user_uuid}"
        proxies = dict(tunnels)
        protocol = "https" if tls else "http"
        for k, v in proxies["ip_list"].items():
            return "%s://%s:%s@%s:%d" % (
                protocol,
                login,
                proxies["agent_key"],
                k if tls else v,
                proxies["port"][self.settings.port_type_choice],
            )

    def generate_session_key(self, timeout: float = 10.0) -> json:
        post_data = {"login": "1", "ver": self.settings.ext_ver}
        return httpx.post(
            f"{self.settings.ccgi_url}background_init?uuid={self.settings.user_uuid}",
            json=post_data,
            headers={"User-Agent": self.settings.user_agent},
            timeout=timeout,
        ).json()["key"]

    def zgettunnels(
        self, session_key: str, country: str, timeout: float = 10.0
    ) -> json:

        qs = {
            "country": country.lower(),
            "limit": 1,
            "ping_id": random.random(),
            "ext_ver": self.settings.ext_ver,
            "browser": self.settings.ext_browser,
            "uuid": self.settings.user_uuid,
            "session_key": session_key,
        }

        return httpx.post(
            f"{self.settings.ccgi_url}zgettunnels", params=qs, timeout=timeout
        ).json()


class Hola:
    def __init__(self, Settings) -> None:
        self.myipUri: str = "https://hola.org/myip.json"
        self.settings = Settings

    def get_country(self) -> str:

        if not self.settings.randomProxy and not self.settings.userCountry:
            self.settings.userCountry = httpx.get(self.myipUri).json()["country"]

        if (
            not self.settings.userCountry in self.settings.zoneAvailable
            or self.settings.randomProxy
        ):
            self.settings.userCountry = random.choice(self.settings.zoneAvailable)

        return self.settings.userCountry