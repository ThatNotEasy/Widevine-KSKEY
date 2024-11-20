import requests
import json

def get_headers():
    headers = {}
    return headers

def get_license(content_id):
    TOKEN = ""
    PARTNER_ID = ""
    url = f"https://api3.hbogoasia.com/v1/movie?contentId={content_id}&territory=MYS"
    response = requests.get(url, headers=get_headers())
    data = response.json()
    content_id = data.get("contentId")
    materials = data.get("materials", [])
    image_href = next((material.get("href") for material in materials if isinstance(material, dict) and material.get("type") == "image"), None)
    genre = data.get("metadata", {}).get("genre")
    title_info = next(iter(data.get("metadata", {}).get("titleInformations", [])), {})
    name = title_info.get("name")
    summary = title_info.get("summary")

    if content_id:
        # REPLACE "{TOKEN}" & "{PARTNER_ID}" WITH YOUR 
        response = requests.get(f"https://api3.hbogoasia.com/v1/asset/playbackurl?territory=MYS&contentId={content_id}&sessionToken={TOKEN}&channelPartnerID={PARTNER_ID}&operatorId=SIN&lang=en", headers=get_headers())
        if response.status_code == 200:
            datas = response.json()
            mpdURL = datas.get("playbackURL")
            license_urls = datas.get("licenseURLs", {}).get("widevine")
            if mpdURL and license_urls:
                cdm = {"license_url": license_urls, "pssh": "AAAAP3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAB8SEJIhyOZ8dW8JT0VCAkLYVg4aBWV6ZHJtSOPclZsG"}
                cdm_headers = {'X-API-KEY': '58146edc021d601f4c6130d7e64062f8168ecc8092a63633bbdd094d7249cbb1', 'Content-Type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
                meow = requests.post("https://dev.kepala-pantas.xyz/dev/widevine/decrypt", json=cdm, headers=cdm_headers)
                meowing = meow.json()
                kid = meowing.get('kid')
                key = meowing.get('keys', [{}])[0].get('key', '').split(':')[1]
                response_data = {"thumbnail": image_href, "title": name, "synopsis": summary, "genre": genre, "kid": kid, "key": key, "mpdURL": mpdURL}
                return json.dumps(response_data, indent=2)
    return None