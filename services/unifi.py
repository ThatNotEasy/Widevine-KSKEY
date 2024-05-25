def get_headers():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,ms;q=0.8",
        "Origin": "https://playtv.unifi.com.my",
        "Referer": "https://playtv.unifi.com.my/",
        "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    return headers

def get_params():
    params = {"deviceId": "YTVjNzVlYzEtMTViNS0zMjBmLThiYTMtZWQ2YmMxNTc4ZGQ5"}
    return params

def get_data():
    data = None
    return data