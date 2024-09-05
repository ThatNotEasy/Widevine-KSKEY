import json

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',  # Updated Content-Type
        'DNT': '1',
        'Origin': 'https://play.starzon.com',
        'Pragma': 'no-cache',
        'Referer': 'https://play.starzon.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_data():
    data = {
        "token": "starzplayarabia|2024-09-05T03:27:29Z|p8lvlUa61MAdgtI0fsUvGAsR3bxdUhvNDjB6Usa3VcWvq2SyOmPYwyKI92X4RkFrgGFBOoWmCjta1hvz8AEh8t/v9UririL9A0ojsFpN4j2alBet70g0/EtiVnLGH7Q4abD9ShVsfmj1LbLoXPh6jV0WniwcXWeYtpU5bHem0QI=|f610dd661bce6b236a71be938d59ba1a9ba2515f",
        "drm_info": [8, 4],
        "kid": "1BAAE328-E893-AF26-9504-4CCF303D5D5E"
    }
    return data