def get_headers():
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzIwODEzNjIxLCJleHAiOjE3MzYzNjU2MjEsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.A3h19FEL9EZja2Pu6zpXV3e2swPlOhUxw3wW-gbkeZMgBoo_Vhs7oXnobJyZ01gQck9aruCZPXe2VAPk1DVpMw',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://tv.apple.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tv.apple.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-apple-music-user-token': 'AmEfgJo5mAqZVMcgQbn+fPzGOcRK/ERmX832HB3IQzx+vj4sT4HxDmpOQm9xoAHu1EcYT7q1UTgi0ItPmvaOjzVAhpQUaiDUBeVIoS5k3Yc4hpz6Yiyi3DV/NnoRlD6lUKEFpBUEn/GqakUpvlK7mEMZ9Zp7+9mMQ2pU9vhRugSat8oswNtnrb5ZU0pM8YyodIH4lBccMIGSSlNar4kBK9189vKT2DbGYN/vK9NJqvwng0k/8g==',
    'x-apple-renewal': 'true',
}
    return headers

def get_data():
    data = {
    'streaming-request': {
        'version': 1,
        'streaming-keys': [
            {
                'challenge': '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',
                'key-system': 'com.widevine.alpha',
                'uri': 'data:text/plain;base64,AAAAOHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABgSEAAAAAA0QY7AYzYgICAgICBI88aJmwY=',
                'id': 0,
                'lease-action': 'start',
                'adamId': '1727880953',
                'isExternal': True,
                'svcId': 'tvs.vds.4073',
            },
        ],
    },
}
    return data