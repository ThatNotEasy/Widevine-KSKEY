import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='WKS-KEYS 2.0 - A tool to obtain Widevine keys from MPD URLs')
    parser.add_argument('-u', '--license-url', required=False, help='URL to request Widevine license')
    parser.add_argument('-m', '--mpd-url', help='URL of the Media Presentation Description (MPD)')
    parser.add_argument('-pp', '--proxy', help='Specify the proxy to use for the requests')
    parser.add_argument('-p', '--pssh', required=False, help='Protection System Specific Header (PSSH)')
    parser.add_argument('-s', '--service', required=True, help='Specify the service module (e.g., prime, netflix)')
    parser.add_argument('-c', '--content-id', required=False, help='Specify the content id for HBOGO modules')
    return parser.parse_args()

