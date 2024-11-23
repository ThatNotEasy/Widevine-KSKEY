import argparse
import sys
from colorama import Fore, Style, init
from modules.utils import banners

# Color Aliases
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
FR = Fore.RESET

# Style Aliases
BR = Style.BRIGHT
DIM = Style.DIM
N = Style.NORMAL

def parse_arguments():
    """Set up argument parsing."""
    # Create an ArgumentParser without the default `-h/--help`
    parser = argparse.ArgumentParser(
        description=f'{Fore.YELLOW}WKS-KEYS 2.0 - A tool for extracting Widevine keys from supported URLs.',
        add_help=False  # Disables the default `-h/--help` option
    )
    parser.add_argument(
        '-u', '--license-url', required=False,
        help=f'{C}The URL to request the Widevine license.{FR}'
    )
    parser.add_argument(
        '-m', '--manifest-url',
        help=f'{C}The URL of the media manifest or content file supported by this tool.{FR}'
    )
    parser.add_argument(
        '-pp', '--proxy',
        help=(
            f'{C}Specify the proxy method to use:\n'
            f'  {Fore.GREEN}"scrape"{FR} - Automatically scrape proxies.\n'
            f'  {Fore.GREEN}"rotate"{FR} - Use rotating proxies.\n'
            f'  {Fore.GREEN}<country_code>{FR} - Use proxies from the specified country.'
        )
    )
    parser.add_argument(
        '-cc', '--country-code', type=str,
        help=f'{C}The country code to use when scraping proxies (e.g., US, GB).{FR}'
    )
    parser.add_argument(
        '-p', '--pssh', required=False,
        help=f'{C}The Protection System Specific Header (PSSH) in base64 format.{FR}'
    )
    parser.add_argument(
        '-s', '--service', required=False,
        help=f'{C}Specify the service module to use (e.g., prime, netflix).{FR}'
    )
    parser.add_argument(
        '-k', '--kid',
        help=f'{C}The Key Identifier (KID) of the media content.{FR}'
    )
    parser.add_argument(
        "-lt", "--lr-token",
        help=f'{C}The login token. Note: Using this may result in your account being blocked.{FR}'
    )
    parser.add_argument(
        '-c', '--content-id', required=False,
        help=f'{C}The content ID to use for HBO GO modules.{FR}'
    )
    parser.add_argument(
        '-d', '--downloads', action='store_true',
        help=f'{C}Enable the download process for the requested media.{FR}'
    )
    parser.add_argument(
        '-o', '--output', required=False,
        help=f'{C}The name of the output file for the extracted keys or media.{FR}'
    )
    parser.add_argument(
        '-H', '--header', action='append',
        help=f'{C}Specify custom HTTP headers in the format "Key: Value".{FR}'
    )
    return parser


def print_custom_help():
    """Print a custom help message."""
    banners()
    print("-" * 100)
    options = [
        (f"{G}-u, --license-url,{FR}", f"{Y}The URL to request the Widevine license.{FR}"),
        (f"{G}-m, --manifest-url,{FR}", 
        f"{Y}The URL of the media manifest or content file supported by this tool.{FR}\n"
        f"{FR}{'-' * 100}{FR}"),
        (f"{G}-pp, --proxy,{FR}", 
        f"{Y}Specify the proxy method to use:{FR}\n"
        f'                     {G}"scrape"{FR} - Automatically scrape proxies.\n'
        f'                     {G}"rotate"{FR} - Use rotating proxies.\n'
        f'                     {G}<country_code>{FR} - Use proxies from the specified country.\n'
        f"{G}-cc, --country-code,{FR} The country code to use when scraping proxies (e.g., US, GB).{FR}\n"
        f"{FR}{'-' * 100}{FR}"),
        (f"{G}-p, --pssh,{FR}", f"{Y}The Protection System Specific Header (PSSH) in base64 format.{FR}"),
        (f"{G}-s, --service,{FR}", f"{Y}Specify the service module to use (e.g., prime, netflix).{FR}"),
        (f"{G}-k, --kid,{FR}", f"{Y}The Key Identifier (KID) of the media content.{FR}"),
        (f"{G}-lt, --lr-token,{FR}", 
        f"{Y}The login token. Note: Using this may result in your account being blocked.{FR}"),
        (f"{G}-c, --content-id,{FR}", 
        f"{Y}The content ID to use for HBO GO modules.{FR}"),
        (f"{G}-d, --downloads,{FR}", 
        f"{Y}Enable the download process for the requested media.{FR}"),
        (f"{G}-o, --output,{FR}", 
        f"{Y}The name of the output file for the extracted keys or media.{FR}"),
        (f"{G}-H, --header,{FR}", 
        f"{Y}Specify custom HTTP headers in the format {G}'Key: Value'{FR}."),
    ]
    for opt, desc in options:
        print(f"{opt.ljust(30)} {desc}")
    print("\n")