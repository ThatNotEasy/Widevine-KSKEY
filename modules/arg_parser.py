import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='WKS-KEYS 2.0 - A tool to obtain Widevine keys from MPD URLs')
    parser.add_argument('-u', '--license-url', required=False, help='URL to request Widevine license')
    parser.add_argument('-m', '--mpd-url', help='URL of the Media Presentation Description (MPD)')
    parser.add_argument('-pp', '--proxy', help=(
        'Specify the proxy to use for the requests. Options: \n'
        '"scrape" to automatically scrape proxies, \n'
        '"rotate" to rotate proxies, \n'
        'or specify a country code to use proxies from that country.'
    ))
    parser.add_argument('-p', '--pssh', required=False, help='Protection System Specific Header (PSSH)')
    parser.add_argument('-s', '--service', required=False, help='Specify the service module (e.g., prime, netflix)')
    parser.add_argument('-c', '--content-id', required=False, help='Specify the content id for HBOGO modules')
    parser.add_argument('-H', '--header', action='append', help='Specify headers in the format "Key: Value"')
    return parser.parse_args()