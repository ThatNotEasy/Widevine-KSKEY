import base64

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://mubi.com',
        'Referer': 'https://mubi.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'dt-custom-data': 'eyJ1c2VySWQiOjE2OTA2MjkxLCJzZXNzaW9uSWQiOiI4ZmY1MGRhYzM1YjdjNDNkZWVlOGFhMmJiNDM0Yzg1OTEwMWY4MzMiLCJtZXJjaGFudCI6Im11YmkifQ==',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return headers


data = None