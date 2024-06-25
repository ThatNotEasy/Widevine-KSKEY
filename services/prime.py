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
        'session-token': 'uTof+99cLOmTxD33bxzOgilyMV1cl1QZptbsjeiS1ikdKMmUSIGjZlMF3FPs40/iSB5UyHVj4Ze8Mvg1i4i9ZV2yrkfRPuYUdU6nVpMwxI+Ivy4BCky7z4UVVmmXrZRXOnNUZvmz+9Ivhvl2FAJmErrpZ/G/NvqQ+lnkxyucIKQIaQ12+VWXxQhM5m6/9troGpKzFLckTVoA/W4Rf9nPGarSGHoIjbMvaqdVSpK+XVKGMEfhXX73Ve9O09eJOLhpfeWN23+ZrTAhuCGCIrgpWrWH+EmGiiwAlC8mINLmdukO3Gu1QR7S05t6CmmFMeU/0UI6mTuH71iggDjnB213X3LHmtFMNczV9q8Gi/F+TF/lR6HiWyQrw88EJXhE+x+8',
    }
    return cookies

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'session-id=140-7704801-4605024; ubid-main=132-8359302-9762828; i18n-prefs=USD; aws-target-data=%7B%22support%22%3A%221%22%7D; regStatus=pre-register; aws-target-visitor-id=1716865194428-493747.48_0; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19881%7CMCMID%7C74230381077583681551112385969525193717%7CMCAID%7CNONE%7CMCOPTOUT-1717701113s%7CNONE%7CvVersion%7C4.4.0; x-main=6pRfCUELnrCwGhfTuYvcBoQ8RNSxLbaqhJ1JDHtwgCkyQBpBspneyP5uAmPO7RyF; at-main=Atza|IwEBIGXidv6PTd0ZKZIR2Sg9I4JEodG_iUo_YUMAmJTtsF38ZtbaoI5-4r6h9vYvt3tBZiQfcYqU2l_O8hPCe-dvDlHCJKzdK_LC2I-LF8QoCQDP6qG54Cc1M6xhN9DpkDosGgDdq7pNDPYZ1FlQQwSnPi6MFtdb-8-D-7Ya80cOLRQA22ZWdN8QoBsThud2cVnM4B2W1MPcvwZjj-mbTnyS2CFRBJt5kjxGfgfCUhWrGu7AQP8JtGpLfoC4ainyCaHqxm0; sess-at-main="K+2VzfazK5PqhY8KM1hNvTflPsvFVMTz8nrZxA0vBxs="; lc-main=en_US; session-id-time=2082787201l; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTEyWThMN04xUU1LQVImdGltZXN0YW1wPTE3MTkwMzMxMTg1NjMmdmVyc2lvbj12MQ.g53dyJRKyeaouex-lcAL_Ebe4JfKghbEiDej51gMV_PaAAAAAQAAAABmdl0ecmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; av-timezone=Asia/Kuala_Lumpur; session-token=uTof+99cLOmTxD33bxzOgilyMV1cl1QZptbsjeiS1ikdKMmUSIGjZlMF3FPs40/iSB5UyHVj4Ze8Mvg1i4i9ZV2yrkfRPuYUdU6nVpMwxI+Ivy4BCky7z4UVVmmXrZRXOnNUZvmz+9Ivhvl2FAJmErrpZ/G/NvqQ+lnkxyucIKQIaQ12+VWXxQhM5m6/9troGpKzFLckTVoA/W4Rf9nPGarSGHoIjbMvaqdVSpK+XVKGMEfhXX73Ve9O09eJOLhpfeWN23+ZrTAhuCGCIrgpWrWH+EmGiiwAlC8mINLmdukO3Gu1QR7S05t6CmmFMeU/0UI6mTuH71iggDjnB213X3LHmtFMNczV9q8Gi/F+TF/lR6HiWyQrw88EJXhE+x+8',
        'Origin': 'https://www.amazon.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.amazon.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Kali Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.142 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_params():
    params = {
        'deviceID': '352ce6da-eb9a-4a7a-a6e8-90aa725b2c60',
        'deviceTypeID': 'AOAGZA014O5RE',
        'gascEnabled': 'true',
        'marketplaceID': 'ATVPDKIKX0DER',
        'uxLocale': 'en_US',
        'firmware': '1',
        'playerType': 'xp',
        'operatingSystemName': 'Linux',
        'operatingSystemVersion': 'unknown',
        'deviceApplicationName': 'Chrome',
        'asin': 'amzn1.dv.gti.34721e3d-35a5-44f1-bbd1-30a7e0d7e3d5',
        'consumptionType': 'Streaming',
        'desiredResources': 'Widevine2License',
        'resourceUsage': 'ImmediateConsumption',
        'videoMaterialType': 'LiveStreaming',
        'clientId': '9ee9ba9b-f89c-41bb-8aa0-4db6e7f24cad',
        'userWatchSessionId': 'ec16549e-c081-4d9f-91c3-9ce9b327b6d7',
        'displayWidth': '1680',
        'displayHeight': '1050',
        'supportsVariableAspectRatio': 'true',
        'supportsEmbeddedTimedTextForVod': 'false',
        'deviceProtocolOverride': 'Https',
        'vodStreamSupportOverride': 'Auxiliary',
        'deviceStreamingTechnologyOverride': 'DASH',
        'deviceDrmOverride': 'CENC',
        'deviceAdInsertionTypeOverride': 'SSAI',
        'deviceHdrFormatsOverride': 'None',
        'deviceVideoCodecOverride': 'H264',
        'deviceVideoQualityOverride': 'HD',
        'deviceBitrateAdaptationsOverride': 'CVBR,CBR',
        'supportsEmbeddedTrickplayForVod': 'false',
        'playerAttributes': '{"middlewareName":"Chrome","middlewareVersion":"125.0.6422.142","nativeApplicationName":"Chrome","nativeApplicationVersion":"125.0.6422.142","supportedAudioCodecs":"AAC","frameRate":"SFR","H264.codecLevel":"3.1","H265.codecLevel":"0.0","AV1.codecLevel":"0.0"}',
    }
    return params

def get_data():
    data = {
        'widevine2Challenge': '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',
        'includeHdcpTestKeyInLicense': 'true',
    }
    return data