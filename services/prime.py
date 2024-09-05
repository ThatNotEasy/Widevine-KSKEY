def get_cookies():
    cookies = {
        'session-id': '262-0012187-9390310',
        'i18n-prefs': 'GBP',
        'ubid-acbuk': '262-7578955-3394923',
        'av-timezone': 'Asia/Kuala_Lumpur',
        'lc-acbuk': 'en_GB',
        'x-acbuk': '"tcEG9fMyzauwD2U4TO2@7fPZ1FAQrzsnuHDp1PDkzlkzVIEfIZLwM?m@InPGqkfX"',
        'at-acbuk': 'Atza|IwEBIB3ymH4AVk5quqx00d3yF9RFIOqk39lfcTURCDF59AK8eAKUzBBblCBKd425ea_bUIeTNZLy31Q1vrPyXyqrALBViZqzZxC7KSje5u15LSyKIZmhpKw2nveDYLp1heLwnqWhJK_aRxezRr6GWRUbNcpafU4-_hzsC9GSpsUq3c6QQsLv-5jIa3nk31lzSRk0eiWDuva557fMRFuTWOBdHLvPKxWEwrNUA3XVvtDWT2TzfQ',
        'sess-at-acbuk': '"i9E5SnB+pZPdrWekMS8fKF/8zL9gpIrmJn3qeDQ6sE4="',
        'sst-acbuk': 'Sst1|PQHLBKloUIllhpT4E0exaZmWCVE2AQo7YZbMBzsQ2ozN31bhg9RRWzKe-TJ1lS_WTf39WBlpod_daB3QsxHXFxW5R4X17tCGOchlOWqvCLOt9lmEPgQnvWQQg-5ppfY4Es41f3pBI34HvpIZB-XmWi08ckyLy8AejUGPp2gqpik567DAnR9-EgZJZEsZjwVgWkMdxuZ8OcuyeR1lifx93uySTFndS4PC-MyNcI4WLOicpuvipqyCeQAP0j_SljdiaSDACxrwORpyrmxuKy9wNVnob6w3QI4CijfxccGYDD52mmo',
        'session-id-time': '2082787201l',
        'av-profile': 'cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTJZUzVXVUJESDAxMzMmdGltZXN0YW1wPTE3MjQzNzExNzUxNjMmdmVyc2lvbj12MQ.g6_Gs4pkWWGnjE9u7NJjztDPNWqOhIcS2LNpbi3WwlJhAAAAAQAAAABmx9DncmF3AAAAAPgWC9WfHH8iB-olH_E9xQ',
        'session-token': '"BtwpFV/THQHC8Ms0LfqMDKN0fJvhjxpUmw9V9/fWkNlColIY7adoLsrbt1UqmQQ71Hf16zQQvVcxQHo16VPMeYUUwHu039Y3gwhyByCjkGGaRKepgAUEC5UnuEgCgA18hLBSESj64oihvNg8LlBX1yU5+xfS6rkchdz6EBvFCAhk0vlZOmtxuPltontbFYvdu6sjRWpbjaDp6/qDdxnwviln1IXYKN2C+QNuApePft+5OR2Nfk0ZNYsU+q9iLSauoI7j9eLTQzZm9N57JKqeRs0rViWSJdPOlTeLyCUD/y9HFeJnr+VZvMsY7eovfkQ2W5pQrPgtGLmGAmK12UKJAU9FSk4PXN9rhihLpGpcn5gEdCC8QEnL3LOtUnQAzvxqAAl9ToXt0Yg="',
    }
    return cookies

def get_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'session-id=262-0012187-9390310; i18n-prefs=GBP; ubid-acbuk=262-7578955-3394923; av-timezone=Asia/Kuala_Lumpur; lc-acbuk=en_GB; x-acbuk="tcEG9fMyzauwD2U4TO2@7fPZ1FAQrzsnuHDp1PDkzlkzVIEfIZLwM?m@InPGqkfX"; at-acbuk=Atza|IwEBIB3ymH4AVk5quqx00d3yF9RFIOqk39lfcTURCDF59AK8eAKUzBBblCBKd425ea_bUIeTNZLy31Q1vrPyXyqrALBViZqzZxC7KSje5u15LSyKIZmhpKw2nveDYLp1heLwnqWhJK_aRxezRr6GWRUbNcpafU4-_hzsC9GSpsUq3c6QQsLv-5jIa3nk31lzSRk0eiWDuva557fMRFuTWOBdHLvPKxWEwrNUA3XVvtDWT2TzfQ; sess-at-acbuk="i9E5SnB+pZPdrWekMS8fKF/8zL9gpIrmJn3qeDQ6sE4="; sst-acbuk=Sst1|PQHLBKloUIllhpT4E0exaZmWCVE2AQo7YZbMBzsQ2ozN31bhg9RRWzKe-TJ1lS_WTf39WBlpod_daB3QsxHXFxW5R4X17tCGOchlOWqvCLOt9lmEPgQnvWQQg-5ppfY4Es41f3pBI34HvpIZB-XmWi08ckyLy8AejUGPp2gqpik567DAnR9-EgZJZEsZjwVgWkMdxuZ8OcuyeR1lifx93uySTFndS4PC-MyNcI4WLOicpuvipqyCeQAP0j_SljdiaSDACxrwORpyrmxuKy9wNVnob6w3QI4CijfxccGYDD52mmo; session-id-time=2082787201l; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTJZUzVXVUJESDAxMzMmdGltZXN0YW1wPTE3MjQzNzExNzUxNjMmdmVyc2lvbj12MQ.g6_Gs4pkWWGnjE9u7NJjztDPNWqOhIcS2LNpbi3WwlJhAAAAAQAAAABmx9DncmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; session-token="BtwpFV/THQHC8Ms0LfqMDKN0fJvhjxpUmw9V9/fWkNlColIY7adoLsrbt1UqmQQ71Hf16zQQvVcxQHo16VPMeYUUwHu039Y3gwhyByCjkGGaRKepgAUEC5UnuEgCgA18hLBSESj64oihvNg8LlBX1yU5+xfS6rkchdz6EBvFCAhk0vlZOmtxuPltontbFYvdu6sjRWpbjaDp6/qDdxnwviln1IXYKN2C+QNuApePft+5OR2Nfk0ZNYsU+q9iLSauoI7j9eLTQzZm9N57JKqeRs0rViWSJdPOlTeLyCUD/y9HFeJnr+VZvMsY7eovfkQ2W5pQrPgtGLmGAmK12UKJAU9FSk4PXN9rhihLpGpcn5gEdCC8QEnL3LOtUnQAzvxqAAl9ToXt0Yg="',
        'DNT': '1',
        'Origin': 'https://www.amazon.co.uk',
        'Referer': 'https://www.amazon.co.uk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    return headers

def get_params():
    params = {
        'deviceID': 'fb7b783c-ccf0-4e36-92e3-1698036c19f7',
        'deviceTypeID': 'AOAGZA014O5RE',
        'gascEnabled': 'false',
        'marketplaceID': 'A1F83G8C2ARO7P',
        'uxLocale': 'en_GB',
        'firmware': '1',
        'titleId': 'amzn1.dv.gti.67f58ea1-b13d-44a4-8207-bd4b6bee3fc1',
    }
    return params

def get_data():
    json_data = {
    'includeHdcpTestKey': True,
    'playbackEnvelope': 'eyJ0eXAiOiJwbGVuditqd2UiLCJjdHkiOiJwbGVuditqd3MiLCJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoiYTJ6K3BwX2VuYytzX3AwSUdWeWcifQ.8AdLbFp19oTljK0FwOUVT9_jyB3UlTyan4-SkCFXLt6G_wAXRTZDrl72zeE_T5WQ0B-WYTa9aj12dKqcCVXSjXK5HYhM1-Xj.sEVa_F6OFrs4i1LtDnMwgg.fVFCBjY8ciDerJIa8yg4fmcIrqZQD9VkhGpjaohxzcMCwLAnU-Ab6a6DT05syeOR_cpahz0meUjCUeIsg_-M9Sif7VMR4GnHAZkjvlNERZ7NvOK4Y8UeP2moRVKeVDai7myZfyyY6VITFHY5uD6hcdaYLGbFMpld51PIJ1ONtSq0oQSJrJfVb_mYuD3x6xSLXqpf5faW7_uqlGqtH3SryPXBSIn_o436dF5Co0jxSwaG5-F6B36HVxdjmMYdiZ1Mu0Ua-_wvnTiNOrLCjb5cWhmLwDAXduowDjDOvRaJYZ5fm2N9CZdTK5htWX33PLma-qeKMiy0i4_SX7Zvw_lKpSY9Ybu9Atlc1fIswaMAEPQQ5sgCfDrLwjo2tHRfmIYDQFkS_iErDGPaPQ2zNs_cMW0woyCOL-FTxIzuWgnDT7rXsC9yDB_kd3uKrAs-c_93OGm9ivqavBbttOQm-hSq1ZOslu3hNCKJNefQ9qS8xzt22aldr2SZdTUtwbvUfkOhMoDokD4QePEtMyyZYwI4E4iTCwOQqFtJYibdpp66MSBW5G-ciUaNmKsEudrdcRmEkIno6GQn5EORkr9Hf3bzgDcCeDE2BWzNyqYY2lFfc0MF1wpVkVN6bQIMbA6EdYkEn_ZG9lpv4miW3ZvxUuaQpP7iZydwm8L4E9AN0uxJNnQ8aprarnbtdWR1I_fVLULdHcNsTU3p0D_rZyIyA3KVUwaxjcQ47c69ueLOISbuR3Fm80bEbn4NuSxYqooYk5av5_Tg8ak49nH8g3JFoDbaE5gi3zycwneIC3JCPuuAVXReWdIM6pmSMNKzbKL-ktEK6qRD6CHbkbVxqqtFvVsTtXnrYzKZhYdY82KP98jeuXUT8pejJmZbPF6MV1BbSE9MFcVH5lZ6Vb7D9NmWfIHU31D_FiqtdZJMBqGr8-p8bB4RoCMWm2SU07hbgzOOsABydWSisqrYPvDgCDLQHrZpe3hildTxHvzOND_nwFtQ05efRb2zgw6nFhdOCaom-JXStVH-BIIMw9fda3ogTw612wBNB5Ng8IpK2tCv0uxXN5AITByM-8Y2wCPAlUQsFj0zuFzHB4rdVrdayIYw9M1ynr33fhEPqivEU5HJSbpjbWWaiO_CDfmSb2UiHuxO31tPOwUxG-08l8IRpSrQP7kCMag8oPbxPF7bmH9Uogx6JyJPIdgy_BRLT0JV4AJkYhsWPqaDXRkd7uhW_G8WBhG46luhbw4Jm4Z5_HCTVgU2SUnVj5lwhZbEusqpqcNsADzesArKS3dY7pZnhyr8sBiAi9xj8nmI8GTKegZPoLW4xDvjhS9RtWgZBA7oUS0B-sGF5HfVswLO-Z-QKhAtVWKCTkZ2rz3raK3hnV1V0hEhHV7bETYauvxePvsPzOkMVupCtjpicAV-IKNet2CZ7RxTmlEJJaN0TSSqXjAifp-kIqLn_T0CEJ3oBFNwG4G97QmqpW6xDL74tMFovV7wYeWgJv7EVIsV8A9kcrZ8RiazPezUrRdXAYEgXptS1X-TGJI_Wk_S-ZW1KH-gJWLMsVnpwnH8NRV00pTVmcWWW5URaZSJYAfzBtbrDWPobYPvb2BlRZMu24YuNFjeORqETQEFH7uXP3RyHat9Gi_sx_gHLxjNfIUmJcXoNWrLs3dSsEDVa6h5EXK4OSu-4AKWrEbHZ7bOEqjgI3C0SKZd_k41AJla2x3wX-JNwkhvgOhovhoIDcDM7YdVib3zweiciio3BMeqhmjvMT7ZuDpXP3J6iSdZ8JNer24J9Yy6IoCWYcwl1A0gq_6_oq_zj_uTm6YNaX-FrB-kgoW_GRS7PVmht60QiVdLNvtqRSVL0QEWm19WLm-csaLq7kS2Wq4nSniBOd-Nzg7GjKI-pziNKhLhTtVW24hHpPvBIuHDgYtaI4ZLojSoPKNJlDl4O58iznHI5kbrB8ADxHqGRHWma70_b7nXUIzYVB31vvkEHf_rzrwTmvpgOY1mI6qmrHCEBCeHHozgjogLkYJaXsb40nCAob6Ob9KGipszRpDeBEhqdEIAwCgOzQmflYcq3jaRZh9so7Da-XTVnfZvLk7o2Fgty8sSpPD4RZ7aZ1auYpE2IBmCsD_iner3O2_RFQiBKs5ju3xioGTP0Q5hIPQTcdRARf4kVGAtMt90XlAoY3wrRg35.Hr-3OgwibeixW7hrEueZtG3fPfpjUoEqPxwdsCOb_vk',
    'licenseChallenge': None
}
    return json_data