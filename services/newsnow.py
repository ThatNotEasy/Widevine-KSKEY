import urllib.parse

def get_cookies():
    cookies = {
        'NOWSESSIONID': '',
        'WZRK_G': 'e735455f7eeb4f2fb2ea429c3a8c3105',
        'custtype': 'GkzpakWFd/dX6j5m2DSmnA==',
        '_gcl_au': '1.1.360202448.1715908394',
        '_gid': 'GA1.2.2009590962.1715908396',
        '_ga_M0KZ536RQR': 'GS1.2.1715908399.1.0.1715908399.0.0.0',
        '_fbp': 'fb.1.1715908400262.968204633',
        '_ga_N2B8JMSSW9': 'GS1.1.1715908393.1.1.1715908414.39.0.0',
        '_ga_K0993SPMC0': 'GS1.1.1715907559.1.1.1715908875.0.0.0',
        '__gads': 'ID=63bd6eba8fe24222:T=1715986354:RT=1715986354:S=ALNI_MbUUeew88p1AbJGrPhqJrF6EYUMIQ',
        '__eoi': 'ID=e4a6dc51b87b497d:T=1715986354:RT=1715986354:S=AA-AfjYRLeGa28E2g3WTrzrvp4Iy',
        '__utma': '249121560.978022773.1715907559.1715986353.1715986353.1',
        '__utmc': '249121560',
        '__utmz': '249121560.1715986353.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '__utmt': '1',
        '_ga': 'GA1.1.978022773.1715907559',
        '_ga_DGFECMB23C': 'GS1.1.1715986353.1.1.1715986364.49.0.0',
        '__utmb': '249121560.2.10.1715986353',
        'iUUID': 'efcaef50816dd41f9514ec460f50fcfc',
        'innity.dmp.0.sess': '1.1715986365615.1715986365615.1715986365615',
        'innity.dmp.0.sess.id': '149138402.0.1715986365615',
        'innity.dmp.cks.innity': '1',
    }
    return cookies

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'NOWSESSIONID=; WZRK_G=e735455f7eeb4f2fb2ea429c3a8c3105; custtype=GkzpakWFd/dX6j5m2DSmnA==; _gcl_au=1.1.360202448.1715908394; _gid=GA1.2.2009590962.1715908396; _ga_M0KZ536RQR=GS1.2.1715908399.1.0.1715908399.0.0.0; _fbp=fb.1.1715908400262.968204633; _ga_N2B8JMSSW9=GS1.1.1715908393.1.1.1715908414.39.0.0; _ga_K0993SPMC0=GS1.1.1715907559.1.1.1715908875.0.0.0; __gads=ID=63bd6eba8fe24222:T=1715986354:RT=1715986354:S=ALNI_MbUUeew88p1AbJGrPhqJrF6EYUMIQ; __eoi=ID=e4a6dc51b87b497d:T=1715986354:RT=1715986354:S=AA-AfjYRLeGa28E2g3WTrzrvp4Iy; __utma=249121560.978022773.1715907559.1715986353.1715986353.1; __utmc=249121560; __utmz=249121560.1715986353.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _ga=GA1.1.978022773.1715907559; _ga_DGFECMB23C=GS1.1.1715986353.1.1.1715986364.49.0.0; __utmb=249121560.2.10.1715986353; iUUID=efcaef50816dd41f9514ec460f50fcfc; innity.dmp.0.sess=1.1715986365615.1715986365615.1715986365615; innity.dmp.0.sess.id=149138402.0.1715986365615; innity.dmp.cks.innity=1',
        'Origin': 'https://news.now.com',
        'Referer': 'https://news.now.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    return headers

def get_data():
    data = '{"rawLicenseRequestBase64": None, "drmToken":"a8b5a79ebd345aee3c622b9d71b6ad370bc65ea6d6e2c9c3ac7055ad201115c81df720e61758dcbae4fe5be8a8b1104114ffed22f31fc37b785186012661902d92617792b86d4d36ef23ea3afa3573b37ac5b1a7dd567b515c6489da751b8f45"}'
    parsed_data = urllib.parse.parse_qs(data)
    data_dict = {key: value[0] for key, value in parsed_data.items()}
    return data_dict
