def get_cookies():
    cookies = {
        'session-id': '140-7704801-4605024',
        'ubid-main': '132-8359302-9762828',
        'lc-main': 'en_US',
        'x-main': '"5rAkN1hDB3pH7JHmn1xiQDNpK6xt6jQvG2768jigGp1W?a7mENTjXMhM2X0bTmXx"',
        'at-main': 'Atza|IwEBIO1why5wZAMzwmpMOY2j_D91z5R6E0Fb6w4t3ZJSghae_17NphQDUmpCsNaQSy7dy3fYmgX94SmKc56SA_Lg7iy5yEipozRzkzM1Fp3-kNQwj1nT4BbfUrVGS9hswHeaCjN7M52t5jvoECibvBdoK6P95ryYWKktNYdDpOWREh6D4P9dCGP5Y0qS5ZmHJi1Ffg_-YvvyujlCmF32k0V2wvSnyG4nkZ6KfxGhayGelVLIMw',
        'sess-at-main': '"vplbJkC5ZulV07KX8BdAGdF65mGCGJwc5FMwqpvt5iY="',
        'session-id-time': '2082787201l',
        'session-token': 'fuy/quMhhkrvkcCEaqwsP8ftp8eb23LpnxqH1+DdpTlA0zug+Nm/RsmfV5jRacM0pCaQ2MMFlZAAzwyVWtLDVQcPdgfZadnYKGUGRAg5Y9SaNb9f3f+HrgA6t+DiokUm5NxdETTedO0TgLC6HlKJrPTtDbkPzVpV3yu82rWX1W1IfW1a0LFlMbjXkJuWj2d9bnluKjehuwLhwyCTj04cTD6d1kMWr66NjScNw96LjAOPSWoKxsgHmt+YvCkS9KLtnsSZw34dqj4l2E4Rr3QqRpXbFsAZ9OF3Zq60/gXQtyukfeXYik6ymaNWcX+6MJj0SHT9Yb1aRAICHE8n1ZRqq0XNWXTmh7/RGgRrTiKgPt+uy0MXItS3TA',
        'i18n-prefs': 'USD',
        'sp-cdn': '"L5Z9:MY"',
    }
    return cookies

def get_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'authorization': 'Bearer Atna|EwICIH2LwYt9RsPrzJ4VzG3Xa6KOQ3vcZocwEcXLOxyB254WqnXDgPOs_BM1d7RMhLkgnvALlAigSZIziFJ1nClcGHL8bkJpYexkd0kUwDXV50i1vZ5njAh7fpFrcxT4qhaVUnfvLSZReAXQs7eXvpWo-F14FmvCpZks2A1DbWkU9ZcxgszptrZ6sqJJnbLFfsG0PBcOby1qZjCnq0oKQJKE7OzMmi63ZdfyeUBZSSGJyukUVhXDGES3lwJZSz3uVwYhVeewSH2ajXBqBeYQOOPHdq82h1Pk4Ja-emTwPYYNNH2Ddg',
        'content-encoding': 'amz-1.0',
        'content-type': 'application/json',
        # 'cookie': 'session-id=140-7704801-4605024; ubid-main=132-8359302-9762828; lc-main=en_US; x-main="5rAkN1hDB3pH7JHmn1xiQDNpK6xt6jQvG2768jigGp1W?a7mENTjXMhM2X0bTmXx"; at-main=Atza|IwEBIO1why5wZAMzwmpMOY2j_D91z5R6E0Fb6w4t3ZJSghae_17NphQDUmpCsNaQSy7dy3fYmgX94SmKc56SA_Lg7iy5yEipozRzkzM1Fp3-kNQwj1nT4BbfUrVGS9hswHeaCjN7M52t5jvoECibvBdoK6P95ryYWKktNYdDpOWREh6D4P9dCGP5Y0qS5ZmHJi1Ffg_-YvvyujlCmF32k0V2wvSnyG4nkZ6KfxGhayGelVLIMw; sess-at-main="vplbJkC5ZulV07KX8BdAGdF65mGCGJwc5FMwqpvt5iY="; session-id-time=2082787201l; session-token=fuy/quMhhkrvkcCEaqwsP8ftp8eb23LpnxqH1+DdpTlA0zug+Nm/RsmfV5jRacM0pCaQ2MMFlZAAzwyVWtLDVQcPdgfZadnYKGUGRAg5Y9SaNb9f3f+HrgA6t+DiokUm5NxdETTedO0TgLC6HlKJrPTtDbkPzVpV3yu82rWX1W1IfW1a0LFlMbjXkJuWj2d9bnluKjehuwLhwyCTj04cTD6d1kMWr66NjScNw96LjAOPSWoKxsgHmt+YvCkS9KLtnsSZw34dqj4l2E4Rr3QqRpXbFsAZ9OF3Zq60/gXQtyukfeXYik6ymaNWcX+6MJj0SHT9Yb1aRAICHE8n1ZRqq0XNWXTmh7/RGgRrTiKgPt+uy0MXItS3TA; i18n-prefs=USD; sp-cdn="L5Z9:MY"',
        'csrf-rnd': '1772007037',
        'csrf-token': 'T1NraJMKwd2Ds4ceHVfq0nuvCO1nXQp4lYYRkGy9dzA=',
        'csrf-ts': '1716540955146',
        'origin': 'https://music.amazon.com',
        'priority': 'u=1, i',
        'referer': 'https://music.amazon.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-amz-target': 'com.amazon.digitalmusiclocator.DigitalMusicLocatorServiceExternal.getLicenseForPlaybackV2'
    }
    return headers

def get_data():
    json_data = {
        'DrmType': 'WIDEVINE',
        'licenseChallenge': None,
        'customerId': 'A3BO6QW1NNU0W7',
        'deviceToken': {
            'deviceTypeId': 'A16ZV8BU3SN1N3',
            'deviceId': '13283593029762828',
        },
        'appInfo': {
            'musicAgent': 'Maestro/1.0 WebCP/1.0.15013.0 (1500-c3f5-WebC-f23b-66be9)',
        },
        'Authorization': 'Bearer Atna|EwICIH2LwYt9RsPrzJ4VzG3Xa6KOQ3vcZocwEcXLOxyB254WqnXDgPOs_BM1d7RMhLkgnvALlAigSZIziFJ1nClcGHL8bkJpYexkd0kUwDXV50i1vZ5njAh7fpFrcxT4qhaVUnfvLSZReAXQs7eXvpWo-F14FmvCpZks2A1DbWkU9ZcxgszptrZ6sqJJnbLFfsG0PBcOby1qZjCnq0oKQJKE7OzMmi63ZdfyeUBZSSGJyukUVhXDGES3lwJZSz3uVwYhVeewSH2ajXBqBeYQOOPHdq82h1Pk4Ja-emTwPYYNNH2Ddg',
    }
    return json_data