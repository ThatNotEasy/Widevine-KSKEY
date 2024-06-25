def get_cookies():
    cookies = {
    'OptanonAlertBoxClosed': '2024-06-18T17:46:50.348Z',
    'TS01e9567a': '01d9bbd03a1956211f9a022bdf2f3f8a4354a644b77dde77bd711d08622eb0eba402272f28d05ea44e8e71dac41ed90f86e8ed781a',
    'dtCookie': 'v_4_srv_30_sn_F23E0C5F5E498F75DBA3D9269BA428EC_perc_100000_ol_0_mul_1_app-3A2c673a8fcdb9beeb_0_app-3Aea7c4b59f27d43eb_1',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Jun+19+2024+02%3A01%3A42+GMT%2B0800+(Malaysia+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fe90c7cf-019d-4cbe-bfb6-78c5dde8927a&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false',
    'ACCESSTOKEN': 'eyJ0eXAiOiJKV1QiLCJraWQiOiJvZXNwX3Rva2VuX3Byb2RfMjAyMDA4MTkiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwcC1hcGkub2VzcC5ob3Jpem9uLnR2Iiwic2lkIjoiYjIzNzA0MDlkM2QwNzljNzQ0ZGU5ZDVjYTZiYWYwNDA5OTJhMDc5NzdjNDMyYjVkN2M1NzQyYzVmY2ZmMDJiOCIsImlhdCI6MTcxODczMzcwOSwiZXhwIjoxNzE4NzQwOTA5LCJzdWIiOiIxMjE1OTMzNTZfZ2IifQ.xOTpRJhIkD51E3NObGmwKnUtHy_yEqQMDPqJCPCdZJ0',
    'CLAIMSTOKEN': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VzIjpbIjFlMDhlNDhkNDZiZGRkOWJkMmFmMmE1MmRiZGYyNzdlMmFkOTMyY2MyNTI3MDQwMDkwNTk5ZTUyNDBhZjlmMDciLCI4NTA0NGM5ZjU1NWRhYjVkMzkxYTY3MjAxZWM2YTA2OThjOTY3YjhlNTZiZDJjYjczZDcyNDUzNWMxMzU1OTk2IiwiYWJlMWI5MDc0ODdkODZkODgyMGUxZTFlYjYwMGZkMjM5ZjFhOWJmZWIzMGJmODNkNjUxZGMxMDcyZWY5OTUzMCIsImVjZWRkZDhiZDcxNmJkOTY5ZjY1OTUyMTg4NTM1MWNhNmEzNWU1OWNhYWRhMmJlYzEzNDJjY2U1ZjU4NjQwNDEiXSwiY3VzdG9tZXJJZCI6IjEyMTU5MzM1Nl9nYiIsInByb2ZpbGVzIjpbImIxNzUyNmM3LTlhYTAtNGMwMS1hMTQxLWQwZjU5YjU0ODBjMSJdLCJleHAiOjE3MTg4MjAxMDl9.7xddEbMG9vS7FyJdgWTliqPXvNakMRH5aeaP6zpWtO4',
    }
    return cookies

def get_headers():
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
    # 'cookie': 'OptanonAlertBoxClosed=2024-06-18T17:46:50.348Z; TS01e9567a=01d9bbd03a1956211f9a022bdf2f3f8a4354a644b77dde77bd711d08622eb0eba402272f28d05ea44e8e71dac41ed90f86e8ed781a; dtCookie=v_4_srv_30_sn_F23E0C5F5E498F75DBA3D9269BA428EC_perc_100000_ol_0_mul_1_app-3A2c673a8fcdb9beeb_0_app-3Aea7c4b59f27d43eb_1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+19+2024+02%3A01%3A42+GMT%2B0800+(Malaysia+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fe90c7cf-019d-4cbe-bfb6-78c5dde8927a&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; ACCESSTOKEN=eyJ0eXAiOiJKV1QiLCJraWQiOiJvZXNwX3Rva2VuX3Byb2RfMjAyMDA4MTkiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwcC1hcGkub2VzcC5ob3Jpem9uLnR2Iiwic2lkIjoiYjIzNzA0MDlkM2QwNzljNzQ0ZGU5ZDVjYTZiYWYwNDA5OTJhMDc5NzdjNDMyYjVkN2M1NzQyYzVmY2ZmMDJiOCIsImlhdCI6MTcxODczMzcwOSwiZXhwIjoxNzE4NzQwOTA5LCJzdWIiOiIxMjE1OTMzNTZfZ2IifQ.xOTpRJhIkD51E3NObGmwKnUtHy_yEqQMDPqJCPCdZJ0; CLAIMSTOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkZXZpY2VzIjpbIjFlMDhlNDhkNDZiZGRkOWJkMmFmMmE1MmRiZGYyNzdlMmFkOTMyY2MyNTI3MDQwMDkwNTk5ZTUyNDBhZjlmMDciLCI4NTA0NGM5ZjU1NWRhYjVkMzkxYTY3MjAxZWM2YTA2OThjOTY3YjhlNTZiZDJjYjczZDcyNDUzNWMxMzU1OTk2IiwiYWJlMWI5MDc0ODdkODZkODgyMGUxZTFlYjYwMGZkMjM5ZjFhOWJmZWIzMGJmODNkNjUxZGMxMDcyZWY5OTUzMCIsImVjZWRkZDhiZDcxNmJkOTY5ZjY1OTUyMTg4NTM1MWNhNmEzNWU1OWNhYWRhMmJlYzEzNDJjY2U1ZjU4NjQwNDEiXSwiY3VzdG9tZXJJZCI6IjEyMTU5MzM1Nl9nYiIsInByb2ZpbGVzIjpbImIxNzUyNmM3LTlhYTAtNGMwMS1hMTQxLWQwZjU5YjU0ODBjMSJdLCJleHAiOjE3MTg4MjAxMDl9.7xddEbMG9vS7FyJdgWTliqPXvNakMRH5aeaP6zpWtO4',
    'devicename': 'My%20Computer%20-%20Google%20Chro',
    'origin': 'https://virgintvgo.virginmedia.com',
    'priority': 'u=1, i',
    'referer': 'https://virgintvgo.virginmedia.com/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-drm-schemeid': 'edef8ba9-79d6-4ace-a3c8-27dcd51d21ed',
    'x-go-dev': 'bb45c46c-3847-4e62-80e4-fd3a94fc8123',
    'x-profile': 'b17526c7-9aa0-4c01-a141-d0f59b5480c1',
    'x-streaming-token': 'YXNzVHlwPU9yaW9uLURBU0gmYy1pcC11bmxvY2tlZD0xJmNvbklkPTE0NjUmY29uVHlwZT00JmN1c0lkPTEyMTU5MzM1Nl9nYiZkZXZGYW09d2ViLWRlc2t0b3AmZHI9MSZkcm1Db25JZD1WTTE0NjUmZHJtRGV2SWQ9MWUwOGU0OGQ0NmJkZGQ5YmQyYWYyYTUyZGJkZjI3N2UyYWQ5MzJjYzI1MjcwNDAwOTA1OTllNTI0MGFmOWYwNyZleHBpcnk9MTcxODczNDEwOSZmbj1zaGEyNTYmcGF0aFVSST0lMkZsaXZlJTJGZGlzazElMkZWTTE0NjUlMkZnby1kYXNoLWZoZC1hdmMlMkYlMkEmcHJvZmlsZT1iMTc1MjZjNy05YWEwLTRjMDEtYTE0MS1kMGY1OWI1NDgwYzEmcmV1c2U9LTEmc0xpbT0yJnNlc0lkPXo0OHpyeEV2bTJ5V0RKUmI4V1pYYTFoWUNZeU1wUDduTzBEdyZzZXNUaW1lPTE3MTg3MzM5NTkmc3RyTGltPTIsZmQ2YTM2MmVmOTdiNjdmNDBkOGRmYmU0NDRmOGQyYjk4MGJhYjgwNDNlMTgzYjdhOTYwMWE1MWJlMGIwNmQxZg==',
    'x-tracking-id': '51300db12d9b7398a7984192ab3a8152b7290ad3d7af4242af0cc6b3e356d23c',
    'content-type': 'application/x-www-form-urlencoded',
    }
    return headers

def get_params():
    params = {
        'ContentId': 'VM1465',
    }
    return params

def get_data():
    data = None
    return data