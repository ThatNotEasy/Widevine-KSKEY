import requests, json
import base64
import logging
import coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

API_KEY = "IJwtS8C9Z7XYLoRmHjmFAyxPZZCGeF7xy1R0o0yy5gtRDR2bA9VUY8DtesVn2xDC"

def get_otp():
    headers = {'Accept': 'application/json','Authorization': f'Apisecret {API_KEY}','Content-Type': 'application/json',}
    json_data = {'ttl': 300,}
    response = requests.post('https://dev.vdocipher.com/api/videos/b0c4d6f3ce4b45e397cfb33b6b023a79/otp', headers=headers, json=json_data)
    print(response.text)
    
def get_token():
    cookies = {
        '_gid': 'GA1.2.1422618089.1723434819',
        '_hjSession_703525': 'eyJpZCI6IjJhY2Y0ZTJmLTFmZWQtNGI1Mi1iZTlmLWU1NzhmN2NlODM1MiIsImMiOjE3MjM0MzQ4MTkzMDAsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxfQ==',
        'ajs_anonymous_id': 'e2c836fd-92e0-4917-a1cc-e57312bae9e2',
        '__zlcmid': '1NDmwCcvzW0WZkf',
        '_lfa': 'LF1.1.aa0e0b55cfd6eb5f.1723435741564',
        '_hjSessionUser_703525': 'eyJpZCI6Ijc3OGI5ZGVmLWFhMTktNTExNy1iODdjLTA5ZDMwNzQ4YWU4YyIsImNyZWF0ZWQiOjE3MjM0MzQ4MTkyOTksImV4aXN0aW5nIjp0cnVlfQ==',
        'vdoToken': '4327b30c194a4bc49153774db2db6505',
        'projectUuid': 'e8ee4841436b4c5aa0926fbb5cb25a1d',
        '_ga': 'GA1.2.272533163.1723434819',
        'ajs_user_id': '291855b2f98e440ea44161356bf02c57',
        'ajs_group_id': 'e8ee4841436b4c5aa0926fbb5cb25a1d',
        '_ga_9BRV3DFFQZ': 'GS1.1.1723434818.1.1.1723436583.11.0.0',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.vdocipher.com',
        'referer': 'https://www.vdocipher.com/dashboard/page/1',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'vdo-dashboard-version': '782c76bd',
        'x-vdo-project': 'e8ee4841436b4c5aa0926fbb5cb25a1d',
    }

    json_data = {'whitelisthref': 'www.vdocipher.com',}
    response = requests.post(f'https://www.vdocipher.com/api/videos/b0c4d6f3ce4b45e397cfb33b6b023a79/token', cookies=cookies, headers=headers, json=json_data)
    print(response.text)
    return response.json()["token"]

def get_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://player.vdocipher.com',
        'priority': 'u=1, i',
        'referer': 'https://player.vdocipher.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
        'vdo-sdk': 'VdoWeb/2.5.2',
    }
    return headers

def get_data(challenge_b64):
    data = {
        "playbackInfo": 'eyJ2aWRlb0lkIjoiYjBjNGQ2ZjNjZTRiNDVlMzk3Y2ZiMzNiNmIwMjNhNzkifQ==',
        "otp": "20160313versASE323hdLjHB1gikEUZ2YVAsNvwZKMVtxNzcelE5BC2qxBym954A",
        "href": "https://visionias.in/",
        "tech": "wv",
        "licenseRequest": challenge_b64
    }
    json_data = json.dumps(data)
    meow = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    response_data = {'token': meow}
    return response_data