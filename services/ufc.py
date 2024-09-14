def get_headers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/124.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkY2UudWZjIiwiZWlkIjoiMmQ2M2QzYjAtZjBiYy00ZGNlLTkzZjQtNDUwYTFkYzJhNDhkIiwiZGVmIjoic2QiLCJwbGMiOmZhbHNlLCJkdHkiOiJCUk9XU0VSIiwiZXhwIjoxNzI2MzE5MjM2LCJpYXQiOjE3MjYyOTc2MzYsImFpZCI6ImZUY358OGM3MmJjNTgtOTlhYy00MmY2LWFjZmQtZTIyNWVhYjljYWE1IiwianRpIjoiNjQ3ZjJiZWItN2VlOS00ZTdiLTk1OWQtNjZiYzNkZTFiODQ4IiwiZGlkIjoiYzhmZDFmMWItMzk0NC00YWViLTkxZjktM2E0MTUxNTdlNDBjIiwiY2lkIjoiZGNlLnVmYyIsInNpZCI6IjMzYjEyYjYxLTYyMDMtNDc3MC05ZmEwLWFhYzYxZmM0ODBiNyJ9.NxicsQV-fwjGnRwtnWiI1lwzZItmx8ReZQoUrQNMuo8',
        'X-DRM-INFO': 'eyJzeXN0ZW0iOiJjb20ud2lkZXZpbmUuYWxwaGEifQ==',
        'Origin': 'https://ufcfightpass.com',
        'Connection': 'keep-alive',
        'Referer': 'https://ufcfightpass.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    return headers