def get_headers():
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/124.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'authorization': 'Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjJXZlVweldreUxEcS1aOXkyRG1Yb0VwNXM3SHBYd3FnZGluallsS3c5NWsifQ.eyJ1c2VyIjoiN2UwMzZhYmItNzFmOS00ODAyLWFkN2EtMjc0NjEyY2VmNzg3IiwiaXNzdWVkIjoxNzI1ODQ1NjE2LCJ1c2Vyc3RhdHVzIjoiUGFydGlhbCIsInNvdXJjZVR5cGUiOiJORkwiLCJwcm9kdWN0U3RhdHVzIjp7IlRlbm5pc1RWIjoiUGFydGlhbCIsIkZJQkEiOiJQYXJ0aWFsIiwiTGlnYVNlZ3VuZGEiOiJQYXJ0aWFsIiwiUmFsbHlUViI6IlBhcnRpYWwiLCJORkwiOiJBY3RpdmVQYWlkIiwiUEdBIjoiUGFydGlhbCIsIkRBWk4iOiJQYXJ0aWFsIn0sInZpZXdlcklkIjoiMjc0NjEyY2VmNzg3IiwiY291bnRyeSI6Im15IiwiY29udGVudENvdW50cnkiOiJteSIsImlzUHVyY2hhc2FibGUiOnRydWUsImhvbWVDb3VudHJ5IjoibXgiLCJ1c2VyVHlwZSI6MywiZGV2aWNlSWQiOiI3ZTAzNmFiYi03MWY5LTQ4MDItYWQ3YS0yNzQ2MTJjZWY3ODctMDA3ZmFiOTIwNCIsImlzRGV2aWNlUGxheWFibGUiOmZhbHNlLCJwbGF5YWJsZUVsaWdpYmlsaXR5U3RhdHVzIjoiRUxJR0lCTEUiLCJjYW5yZWRlZW1nYyI6IkVuYWJsZWQiLCJqdGkiOiI4MDlmMmY2Ni00MTM5LTQ0ZGUtODFiOC02YTRiNDc2OTU1MWEiLCJpZHBUeXBlIjoiaWRwLXBhc3N3b3JkIiwicHJvdmlkZXJOYW1lIjoiZGF6biIsInByb3ZpZGVyQ3VzdG9tZXJJZCI6IjgzNDhkODg1LWUwMTktNGY5Zi04YThhLTNmMTE4YTk4YWQ0ZSIsImVudGl0bGVtZW50cyI6eyJlbnRpdGxlbWVudFNldHMiOlt7ImlkIjoidGllcl9uZmxfcHJvIiwicHJvZHVjdFR5cGUiOiJ0aWVyIiwiZW50aXRsZW1lbnRzIjpbImVudF9uZmxfcHJvIiwiZW50aXRsZW1lbnRfbXVsdGlwbGVfZGV2aWNlc18yMCIsImVudGl0bGVtZW50X2FsbG93X2Rvd25sb2FkIl19XSwiZmVhdHVyZXMiOnsiREVWSUNFIjp7ImFjY2Vzc19kZXZpY2UiOiJhbnkiLCJtYXhfcmVnaXN0ZXJlZF9kZXZpY2VzIjoyMH0sIkNPTkNVUlJFTkNZIjp7Im1heF9kZXZpY2VzIjoyfSwiRE9XTkxPQUQiOnRydWV9fSwibGlua2VkU29jaWFsUGFydG5lcnMiOltdLCJleHAiOjE3MjU4NTI4MTYsImlzcyI6Imh0dHBzOi8vYXV0aC5hci5pbmRhem4uY29tIn0.humOwHWX3BhYPSd5ZQGfbTQaTOqSQUU28ZPiCbu83Q2DaaXZdwS7WUiwsd7-oetf6hEMBQjcA1i4OKJPkraP4T3-AoviY80f8AK--Hh6bipeYgvbzndMSXJAxw-1s-AMcf9kNN3KIid6ArQCV2DbMtL3GYKQdMzuV3aITeBdyUSNDR1HU0Z01HT_w4d2oANJXBFzrXX84oC98JNbJNb8LGXHtVjMhlSVKa6I8rmHEHp8zxvTos7dw6DZJnyg0pv_SlYlmsxcjDrNRdBoVGm8VYHMzehmCrmAIjjx9D35XtGtzqCptHo1Ee6yGqfQv7A2I1PIQCuD7eUXlCvuuP9e4w',
    'Content-Type': 'application/octet-stream',
    'x-correlation-id': '615ca08f-64ee-46e5-b340-258ce5f4f3d8',
    'Origin': 'https://www.dazn.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.dazn.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}
    return headers

def get_params():
    params = {
    'legacyContentId': 'prod-live1',
    'contentId': '247Channel023_catchup',
    'platform': 'web',
    'manufacturer': 'unknown',
    'model': 'unknown',
    'appVersion': '0.46.2',
    'uid': '7e036abb-71f9-4802-ad7a-274612cef787',
    'accountStatus': 'Partial',
    'assetId': 'pzv0wy4hli7k1rus65ptuyz68',
    'tid': '0966aaa9-5701-43b0-a33d-20b6ca07716f',
    'uexp': '1725932057330',
    'mediaType': 'live',
    'mediaId': '247Channel023_catchup',
    'metadata': 'country=my',
    'hash': '12d8c0c89f0b38ba122d4b24d888c97d5784afc418a7439acd2899368bd76b92',
}
    return params

def get_data():
    data = None
    return data