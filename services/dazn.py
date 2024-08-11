def get_headers():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ms;q=0.8',
        'authorization': 'Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjJXZlVweldreUxEcS1aOXkyRG1Yb0VwNXM3SHBYd3FnZGluallsS3c5NWsifQ.eyJ1c2VyIjoiMTMxNTMxZWUtOTVlYi00MTZiLWFhYjktNWFkMjQyN2E4ZjhlIiwiaXNzdWVkIjoxNzIzMzg1MTU2LCJ1c2Vyc3RhdHVzIjoiQWN0aXZlUGFpZCIsInNvdXJjZVR5cGUiOiIiLCJwcm9kdWN0U3RhdHVzIjp7Ik5GTCI6IlBhcnRpYWwiLCJEQVpOIjoiQWN0aXZlUGFpZCJ9LCJ2aWV3ZXJJZCI6IjVhZDI0MjdhOGY4ZSIsImNvdW50cnkiOiJteSIsImNvbnRlbnRDb3VudHJ5IjoibXkiLCJpc1B1cmNoYXNhYmxlIjp0cnVlLCJob21lQ291bnRyeSI6Im5sIiwidXNlclR5cGUiOjMsImRldmljZUlkIjoiMTMxNTMxZWUtOTVlYi00MTZiLWFhYjktNWFkMjQyN2E4ZjhlLTAwMTMzNDhkYmIiLCJpc0RldmljZVBsYXlhYmxlIjp0cnVlLCJwbGF5YWJsZUVsaWdpYmlsaXR5U3RhdHVzIjoiUExBWUFCTEUiLCJjYW5yZWRlZW1nYyI6IkVuYWJsZWQiLCJqdGkiOiJmYjU4N2E1YS1iNjdlLTQwMTgtODRmNi02NGJkZjNmNWZjZjUiLCJpZHBUeXBlIjoiaWRwLXBhc3N3b3JkIiwicHJvdmlkZXJOYW1lIjoiZGF6biIsInByb3ZpZGVyQ3VzdG9tZXJJZCI6IjM1NjI3OGU1LTRkMWYtNGQ1Ny04YTdmLTgyMDNiY2Y3MGU3MCIsImVudGl0bGVtZW50cyI6eyJlbnRpdGxlbWVudFNldHMiOlt7ImlkIjoiYmFzZV9lbnRfc2V0IiwicHJvZHVjdFR5cGUiOiJ0aWVyIiwiZW50aXRsZW1lbnRzIjpbImJhc2VfZGF6bl9jb250ZW50IiwiZW50aXRsZW1lbnRfYWxsb3dfd2F0Y2hfY29uY3VycmVuY3kiLCJlbnRpdGxlbWVudF9tdWx0aXBsZV9kZXZpY2VzXzk5OSJdfSx7ImlkIjoia3NpX3RvbW15X3BhdWxfZGFuaXMiLCJwcm9kdWN0VHlwZSI6InBwdiIsImVudGl0bGVtZW50cyI6WyJrc2lfdG9tbXlfcGF1bF9kYW5pc19jYSIsImtzaV90b21teV9wYXVsX2RhbmlzX3JvdyIsImtzaV90b21teV9wYXVsX2RhbmlzX2JyIiwia3NpX3RvbW15X3BhdWxfZGFuaXNfdHciLCJrc2lfdG9tbXlfcGF1bF9kYW5pc19qcCIsImtzaV90b21teV9wYXVsX2RhbmlzX3VzIiwia3NpX3RvbW15X3BhdWxfZGFuaXNfaXQiLCJrc2lfdG9tbXlfcGF1bF9kYW5pc19yb3dfZ2JfaWUiLCJrc2lfdG9tbXlfcGF1bF9kYW5pc19kZSIsImtzaV90b21teV9wYXVsX2RhbmlzX2VzIiwia3NpX3RvbW15X3BhdWxfZGFuaXNfcHQiLCJrc2lfdG9tbXlfcGF1bF9kYW5pc19iZSIsImtzaV90b21teV9wYXVsX2RhbmlzX3Jvd19mciJdfV0sImZlYXR1cmVzIjp7IkRFVklDRSI6eyJhY2Nlc3NfZGV2aWNlIjoiYW55IiwibWF4X3JlZ2lzdGVyZWRfZGV2aWNlcyI6OTk5fSwiQ09OQ1VSUkVOQ1kiOnsibWF4X2RldmljZXMiOjJ9fX0sImxpbmtlZFNvY2lhbFBhcnRuZXJzIjpbXSwiZXhwIjoxNzIzMzkyMzU2LCJpc3MiOiJodHRwczovL2F1dGguYXIuaW5kYXpuLmNvbSJ9.JaQKu4cseh_Ui8WzCLj13ahpI7rNsrEb0m83fN7hCOmZEfGVjzhGKHXoD70HVjcpFfJXttPFrgrkcmY6H3UxK9O5iBt7npqilbdA4VU65Irm0LsT8pImzGAKvQlgfRbFRVEHovQSh0zyZouZib9WElX2aFn_76O3KLJvEHqqeEGpOs4ck4A1KZa7LGSmZm1YmTPIorgGTfHda0xYGTIFhxTvN3sodVwcPRkEGloFwSHSGWp76xXxWGFnPD9q6TIkAHGjus_kBvAXepQGQBJDs_O7sd_XG3qQnkjdMwoU2MGrQtsBUDXVWELiwW6bzFq_991WfphWcbwyuX2N2kHHTA',
        'content-type': 'application/octet-stream',
        'dnt': '1',
        'origin': 'https://www.dazn.com',
        'priority': 'u=1, i',
        'referer': 'https://www.dazn.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-correlation-id': '7ca5be03-72f6-41d0-82e5-3f263f063515',
    }
    return headers

def get_params():
    params = {
    'legacyContentId': 'prod-live1',
    'contentId': '247Channel023_catchup',
    'platform': 'web',
    'manufacturer': 'microsoft',
    'model': 'unknown',
    'appVersion': '0.42.7',
    'uid': '131531ee-95eb-416b-aab9-5ad2427a8f8e',
    'accountStatus': 'ActivePaid',
    'assetId': 'pzv0wy4hli7k1rus65ptuyz68',
    'tid': 'e66404b4-7bcd-4374-bd02-8f12c79a7b82',
    'uexp': '1723474004124',
    'mediaType': 'live',
    'mediaId': '247Channel023_catchup',
    'metadata': 'country=my',
    'hash': '13d9661557a789597413fb5c259288553f6526836b96b936aaca9bdd34140494',
}
    return params