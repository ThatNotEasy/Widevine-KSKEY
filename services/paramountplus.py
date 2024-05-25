import urllib.parse

def get_headers():
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjNkNjg4NGJmLWViMDktNDA1Zi1hOWZjLWU0NGE1NmY3NjZiNiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMDk0MzQ3MV9VUyIsImVudCI6W3siYmlkIjoiQWxsQWNjZXNzTWFpbiIsImVwaWQiOjh9XSwiaWF0IjoxNzE2NjE2MjEzLCJleHAiOjE3MTY2MzA2MTMsImlzcyI6ImNicyIsImFpZCI6ImNic2kiLCJpc2UiOnRydWUsImp0aSI6ImJhZDkwYTU4LTRiOTMtNDQ4MC04MWQ3LTIyMTBlOTBkZTM3MCJ9.yC-aJOTDSg2XAUeyvhe3VjkGxp8MMrGIKpsYOefeIZk',
    'origin': 'https://www.paramountplus.com',
    'priority': 'u=1, i',
    'referer': 'https://www.paramountplus.com/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}
    return headers

def get_params():
    params = {
        'CrmId': 'cbsi',
        'AccountId': 'cbsi',
        'SubContentType': 'Default',
        'ContentId': 'Cd3Fse6Xve3v7e69nMKZmNchXwEHGvll',
        'CMCD': 'mtp=1300,ot=k,sf=d,sid="349c0ab7-3b5e-4e14-af78-244732fbb542",su',
    }
    encoded_params = urllib.parse.urlencode(params)
    return encoded_params

def get_data():
    data = None
    return data