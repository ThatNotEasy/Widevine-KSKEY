def get_cookies():
    cookies = {
        'i18n-prefs': 'USD',
        'lc-main-av': 'en_US',
        'ubid-main-av': '356-9335829-7077352',
        'av-timezone': 'Asia/Kuala_Lumpur',
        'session-id': '358-0055304-0529671',
        'x-main-av': '"O0cKrrUaLeWhg?Z0pZuGMPabeiZ@buJZwf?6fM7CJAEQK8TVbpZwq7EqmS9pT49u"',
        'session-id-time': '2082787201l',
        'sess-at-main-av': 'mqjA7SnaEdsBwqXRY2nNJPBbN86d1bjXXtpUbbmasvk=',
        'at-main-av': 'Atza|IwEBIMSlpq5nidrkgStTUnRc74l4rYuUY6Q6v5RfRO2v2PY73FyVjOvvkA8g1F4mABNE16fGziKSHmlHYbOgFcAgBpttNP7H2P1Ln0E3UhT0fqm22hrPB6-dr8Q8o3JWhxJBSPZJIVAlra362MNF6fXBn64oWIDDt4s4k6AUCTGdcZgQU_6z38khgxqMeIfkVrCgCXBwZUov4hz2uEy0v-C2R-DVwKfXkuA4HYk1QUfTU3JkE8lUOikEV_9gQNgNkIQ957dx4RUz29dr0XDP47VdOG85h70RqCrNC5MWCFlD6_504NWn23ToQFBOeLTjrB66O0SUf-habnqzYbqT8X67ouKhfhFDWKmrihA-HJdoQRXyJA',
        'av-profile': 'cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTE0R0lVNkNTNkRaQlMmdGltZXN0YW1wPTE3MTc4MDQ1NTU4NTAmdmVyc2lvbj12MQ.g2lcSCr9x0-oGbPWNbK-7wP5iL5rSLbKpSiCUKatm9jEAAAAAQAAAABmY54LcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ',
        'session-token': '"cbIZLktIj2804SucCdi10hsEPyUpWRj5/qHA+I1effdlYetCmZE0y6hGWDutZcECAn0lM3Ln32sv4OnxPggUmjTSuDnZUDBao1dqsizQHfixhokG5RPlhz8uNlfEopehwKzdj1BIVk0H6NVnHAmtWBW/cjBhTkGdL0avMTL4z1rRkeygX4eXUXjSndXrePYIxJvOU5slx1nR6Rz48XFwFkWUWEVZADNJhFt37oDh2uAP8LmFf3CKJylfmM729xRnolzfgj0PpohWJN2zYBxalu1UX4MFQ92xErih3YyRYXh7d0T4o0YF3DSUdqLp2FgWhjfWHgMRHS8p1q1sYvOvofugLa/kZnP9yY8OGg5I+7dCrYENL4llJa5OOLL3gLXRJ+xcYF0lE+QRjju5RHph+QTdzGnen6zWlYWA/WxYlVNBJBdTKEo9fg=="',
    }
    return cookies

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'i18n-prefs=USD; lc-main-av=en_US; ubid-main-av=356-9335829-7077352; av-timezone=Asia/Kuala_Lumpur; session-id=358-0055304-0529671; x-main-av="O0cKrrUaLeWhg?Z0pZuGMPabeiZ@buJZwf?6fM7CJAEQK8TVbpZwq7EqmS9pT49u"; session-id-time=2082787201l; sess-at-main-av=mqjA7SnaEdsBwqXRY2nNJPBbN86d1bjXXtpUbbmasvk=; at-main-av=Atza|IwEBIMSlpq5nidrkgStTUnRc74l4rYuUY6Q6v5RfRO2v2PY73FyVjOvvkA8g1F4mABNE16fGziKSHmlHYbOgFcAgBpttNP7H2P1Ln0E3UhT0fqm22hrPB6-dr8Q8o3JWhxJBSPZJIVAlra362MNF6fXBn64oWIDDt4s4k6AUCTGdcZgQU_6z38khgxqMeIfkVrCgCXBwZUov4hz2uEy0v-C2R-DVwKfXkuA4HYk1QUfTU3JkE8lUOikEV_9gQNgNkIQ957dx4RUz29dr0XDP47VdOG85h70RqCrNC5MWCFlD6_504NWn23ToQFBOeLTjrB66O0SUf-habnqzYbqT8X67ouKhfhFDWKmrihA-HJdoQRXyJA; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTE0R0lVNkNTNkRaQlMmdGltZXN0YW1wPTE3MTc4MDQ1NTU4NTAmdmVyc2lvbj12MQ.g2lcSCr9x0-oGbPWNbK-7wP5iL5rSLbKpSiCUKatm9jEAAAAAQAAAABmY54LcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; session-token="cbIZLktIj2804SucCdi10hsEPyUpWRj5/qHA+I1effdlYetCmZE0y6hGWDutZcECAn0lM3Ln32sv4OnxPggUmjTSuDnZUDBao1dqsizQHfixhokG5RPlhz8uNlfEopehwKzdj1BIVk0H6NVnHAmtWBW/cjBhTkGdL0avMTL4z1rRkeygX4eXUXjSndXrePYIxJvOU5slx1nR6Rz48XFwFkWUWEVZADNJhFt37oDh2uAP8LmFf3CKJylfmM729xRnolzfgj0PpohWJN2zYBxalu1UX4MFQ92xErih3YyRYXh7d0T4o0YF3DSUdqLp2FgWhjfWHgMRHS8p1q1sYvOvofugLa/kZnP9yY8OGg5I+7dCrYENL4llJa5OOLL3gLXRJ+xcYF0lE+QRjju5RHph+QTdzGnen6zWlYWA/WxYlVNBJBdTKEo9fg=="',
        'Origin': 'https://www.primevideo.com',
        'Referer': 'https://www.primevideo.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Kali Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.142 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_params():
    params = {
        'deviceID': '2120b063-7be6-48f4-b967-ba9915e2c24c',
        'deviceTypeID': 'AOAGZA014O5RE',
        'gascEnabled': 'true',
        'marketplaceID': 'A2MFUE2XK8ZSSY',
        'uxLocale': 'en_US',
        'firmware': '1',
        'playerType': 'xp',
        'operatingSystemName': 'Linux',
        'operatingSystemVersion': 'unknown',
        'deviceApplicationName': 'Chrome',
        'asin': 'amzn1.dv.gti.02abea89-4676-521d-dac1-41b4689c7045',
        'consumptionType': 'Streaming',
        'desiredResources': 'Widevine2License',
        'resourceUsage': 'ImmediateConsumption',
        'videoMaterialType': 'Feature',
        'clientId': '9ee9ba9b-f89c-41bb-8aa0-4db6e7f24cad',
        'userWatchSessionId': '898288c4-8917-4db9-91fa-5586695658ff',
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
        'widevine2Challenge': None,
        'includeHdcpTestKeyInLicense': 'true',
    }
    return data