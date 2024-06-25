def get_cookies():
    cookies = {
        'session-id': '140-7704801-4605024',
        'ubid-main': '132-8359302-9762828',
        'i18n-prefs': 'USD',
        'aws-target-data': '%7B%22support%22%3A%221%22%7D',
        'regStatus': 'pre-register',
        'aws-target-visitor-id': '1716865194428-493747.48_0',
        'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C19881%7CMCMID%7C74230381077583681551112385969525193717%7CMCAID%7CNONE%7CMCOPTOUT-1717701113s%7CNONE%7CvVersion%7C4.4.0',
        'x-main': '6pRfCUELnrCwGhfTuYvcBoQ8RNSxLbaqhJ1JDHtwgCkyQBpBspneyP5uAmPO7RyF',
        'at-main': 'Atza|IwEBIGXidv6PTd0ZKZIR2Sg9I4JEodG_iUo_YUMAmJTtsF38ZtbaoI5-4r6h9vYvt3tBZiQfcYqU2l_O8hPCe-dvDlHCJKzdK_LC2I-LF8QoCQDP6qG54Cc1M6xhN9DpkDosGgDdq7pNDPYZ1FlQQwSnPi6MFtdb-8-D-7Ya80cOLRQA22ZWdN8QoBsThud2cVnM4B2W1MPcvwZjj-mbTnyS2CFRBJt5kjxGfgfCUhWrGu7AQP8JtGpLfoC4ainyCaHqxm0',
        'sess-at-main': '"K+2VzfazK5PqhY8KM1hNvTflPsvFVMTz8nrZxA0vBxs="',
        'lc-main': 'en_US',
        'session-id-time': '2082787201l',
        'av-profile': 'cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTEyWThMN04xUU1LQVImdGltZXN0YW1wPTE3MTkwMzMxMTg1NjMmdmVyc2lvbj12MQ.g53dyJRKyeaouex-lcAL_Ebe4JfKghbEiDej51gMV_PaAAAAAQAAAABmdl0ecmF3AAAAAPgWC9WfHH8iB-olH_E9xQ',
        'av-timezone': 'Asia/Kuala_Lumpur',
        'session-token': 'rPOBTA1puV2P5at5UkFEABqD2vSo95I7JQwEIa7MLrRdJ2rUQ+2DMptw0DVbTGuCtzKXOZGZ13SMgOCgNNmoMLGOjwcFvM07rgpTE1jw3i5Ai+gxQyHQ2Ptn8InqNkBi3ETT0E2YYdkF1p4ZdJPUGCzGN1OxIOnpEhBFn+hNBm+A+NhFjwtKxWN9F6G0wbwGdjVd1JmjfZeibAFVmjnh74wSoCpKywEaFRtJrGhH/0b3dlfpTDYyLtiEAMw+x3eIVKnvvWdp9wyl9ZKV3OMFzS4dnC0tFSoHKIKXcumarxi/9WHVuk2khpSfNe+HUfhrp2LvfQiSQ1AxBD6FAba3bWIMrMKDp/fXxPbULBg32cFVvWNASYaXUmP8KlEmEHcS',
    }
    return cookies

def get_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'authorization': 'Bearer Atna|EwICII1y2y3650bjtWEGjIGzu4vkCIwgJx5X8kS44JNZy14GayZiKFydS4r7rKWGSoPKq46lKBKvtkscS8qXDAfGPBrVgwZ5Ytm7H81MsoX-AcaaPoiyr6GOr4t2rFtik3QRtnx-IUi7Iojz_yqP-4E7sTmaUYUmG6E_7CeO2EPDcU55sp3xxoG9HcOQmkv9ev171hQx1SY18Z08XTWoVp_hxq-F3I08f2dvVdMt5TY9kL46iA6pCOVtPTwlJgrdxBFtkYwJWYUPwogJsGKRcyJcgEEGqag4aYRbxU5QRj9jN_11BK4DviySUamfnzs9Hgl9hrM',
        'content-encoding': 'amz-1.0',
        'content-type': 'application/json',
        # 'cookie': 'session-id=140-7704801-4605024; ubid-main=132-8359302-9762828; i18n-prefs=USD; aws-target-data=%7B%22support%22%3A%221%22%7D; regStatus=pre-register; aws-target-visitor-id=1716865194428-493747.48_0; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19881%7CMCMID%7C74230381077583681551112385969525193717%7CMCAID%7CNONE%7CMCOPTOUT-1717701113s%7CNONE%7CvVersion%7C4.4.0; x-main=6pRfCUELnrCwGhfTuYvcBoQ8RNSxLbaqhJ1JDHtwgCkyQBpBspneyP5uAmPO7RyF; at-main=Atza|IwEBIGXidv6PTd0ZKZIR2Sg9I4JEodG_iUo_YUMAmJTtsF38ZtbaoI5-4r6h9vYvt3tBZiQfcYqU2l_O8hPCe-dvDlHCJKzdK_LC2I-LF8QoCQDP6qG54Cc1M6xhN9DpkDosGgDdq7pNDPYZ1FlQQwSnPi6MFtdb-8-D-7Ya80cOLRQA22ZWdN8QoBsThud2cVnM4B2W1MPcvwZjj-mbTnyS2CFRBJt5kjxGfgfCUhWrGu7AQP8JtGpLfoC4ainyCaHqxm0; sess-at-main="K+2VzfazK5PqhY8KM1hNvTflPsvFVMTz8nrZxA0vBxs="; lc-main=en_US; session-id-time=2082787201l; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTEyWThMN04xUU1LQVImdGltZXN0YW1wPTE3MTkwMzMxMTg1NjMmdmVyc2lvbj12MQ.g53dyJRKyeaouex-lcAL_Ebe4JfKghbEiDej51gMV_PaAAAAAQAAAABmdl0ecmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; av-timezone=Asia/Kuala_Lumpur; session-token=rPOBTA1puV2P5at5UkFEABqD2vSo95I7JQwEIa7MLrRdJ2rUQ+2DMptw0DVbTGuCtzKXOZGZ13SMgOCgNNmoMLGOjwcFvM07rgpTE1jw3i5Ai+gxQyHQ2Ptn8InqNkBi3ETT0E2YYdkF1p4ZdJPUGCzGN1OxIOnpEhBFn+hNBm+A+NhFjwtKxWN9F6G0wbwGdjVd1JmjfZeibAFVmjnh74wSoCpKywEaFRtJrGhH/0b3dlfpTDYyLtiEAMw+x3eIVKnvvWdp9wyl9ZKV3OMFzS4dnC0tFSoHKIKXcumarxi/9WHVuk2khpSfNe+HUfhrp2LvfQiSQ1AxBD6FAba3bWIMrMKDp/fXxPbULBg32cFVvWNASYaXUmP8KlEmEHcS',
        'csrf-rnd': '1582155653',
        'csrf-token': 'Dmi7v4Ib51nWTJGSM1rJf4ygIrfCVbkUJk4v3+EoFcg=',
        'csrf-ts': '1719111787272',
        'origin': 'https://music.amazon.com',
        'priority': 'u=1, i',
        'referer': 'https://music.amazon.com/playlists/B01M11SBC8',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-amz-target': 'com.amazon.digitalmusiclocator.DigitalMusicLocatorServiceExternal.getLicenseForPlaybackV2',
        'x-requested-with': 'XMLHttpRequest',
    }
    return headers

def get_data():
    data = {
        'DrmType': 'WIDEVINE',
        'licenseChallenge': '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',
        'customerId': 'A3BO6QW1NNU0W7',
        'deviceToken': {
            'deviceTypeId': 'A16ZV8BU3SN1N3',
            'deviceId': '13283593029762828',
        },
        'appInfo': {
            'musicAgent': 'Maestro/1.0 WebCP/1.0.15193.0 (9517-0ff1-WebC-c9e1-b97c6)',
        },
        'Authorization': 'Bearer Atna|EwICII1y2y3650bjtWEGjIGzu4vkCIwgJx5X8kS44JNZy14GayZiKFydS4r7rKWGSoPKq46lKBKvtkscS8qXDAfGPBrVgwZ5Ytm7H81MsoX-AcaaPoiyr6GOr4t2rFtik3QRtnx-IUi7Iojz_yqP-4E7sTmaUYUmG6E_7CeO2EPDcU55sp3xxoG9HcOQmkv9ev171hQx1SY18Z08XTWoVp_hxq-F3I08f2dvVdMt5TY9kL46iA6pCOVtPTwlJgrdxBFtkYwJWYUPwogJsGKRcyJcgEEGqag4aYRbxU5QRj9jN_11BK4DviySUamfnzs9Hgl9hrM',
    }
    return data