import argparse
import sys
from colorama import Fore, Style, init
from modules.utils import print_title

# Color Aliases
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE

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
        help=f'{Fore.CYAN}The URL to request the Widevine license.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-m', '--manifest-url',
        help=f'{Fore.CYAN}The URL of the media manifest or content file supported by this tool.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-pp', '--proxy',
        help=(
            f'{Fore.CYAN}Specify the proxy method to use:\n'
            f'  {Fore.GREEN}"scrape"{Fore.RESET} - Automatically scrape proxies.\n'
            f'  {Fore.GREEN}"rotate"{Fore.RESET} - Use rotating proxies.\n'
            f'  {Fore.GREEN}<country_code>{Fore.RESET} - Use proxies from the specified country.'
        )
    )
    parser.add_argument(
        '-cc', '--country-code', type=str,
        help=f'{Fore.CYAN}The country code to use when scraping proxies (e.g., US, GB).{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-p', '--pssh', required=False,
        help=f'{Fore.CYAN}The Protection System Specific Header (PSSH) in base64 format.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-s', '--service', required=False,
        help=f'{Fore.CYAN}Specify the service module to use (e.g., prime, netflix).{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-k', '--kid',
        help=f'{Fore.CYAN}The Key Identifier (KID) of the media content.{Style.RESET_ALL}'
    )
    parser.add_argument(
        "-lt", "--lr-token",
        help=f'{Fore.CYAN}The login token. Note: Using this may result in your account being blocked.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-c', '--content-id', required=False,
        help=f'{Fore.CYAN}The content ID to use for HBO GO modules.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-d', '--downloads', action='store_true',
        help=f'{Fore.CYAN}Enable the download process for the requested media.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-o', '--output', required=False,
        help=f'{Fore.CYAN}The name of the output file for the extracted keys or media.{Style.RESET_ALL}'
    )
    parser.add_argument(
        '-H', '--header', action='append',
        help=f'{Fore.CYAN}Specify custom HTTP headers in the format "Key: Value".{Style.RESET_ALL}'
    )
    return parser


def print_custom_help():
    """Print a custom help message."""
    print_title("C1pherForge")
    print("C1pherForge 2.3 - A tool for extracting Widevine keys from supported URLs.\n")
    print("Available Options:")
    print("-" * 100)
    options = [
        (G + "-u, --license-url,", Y + "The URL to request the Widevine license."),
        (G + "-m, --manifest-url,", Y + "The URL of the media manifest or content file supported by this tool.\n"
        '----------------------------------------------------------------------------------------------------'),
        ("-pp, --proxy", 'Specify the proxy method to use:\n'
                        '                               "scrape" - Automatically scrape proxies.\n'
                        '                               "rotate" - Use rotating proxies.\n'
                        '                               <country_code> - Use proxies from the specified country.\n'
                        '-cc, --country-code            The country code to use when scraping proxies (e.g., US, GB).\n'
                        '----------------------------------------------------------------------------------------------------'),
        ("-p, --pssh", "The Protection System Specific Header (PSSH) in base64 format."),
        ("-s, --service", "Specify the service module to use (e.g., prime, netflix)."),
        ("-k, --kid", "The Key Identifier (KID) of the media content."),
        ("-lt, --lr-token", "The login token. Note: Using this may result in your account being blocked."),
        ("-c, --content-id", "The content ID to use for HBO GO modules."),
        ("-d, --downloads", "Enable the download process for the requested media."),
        ("-o, --output", "The name of the output file for the extracted keys or media."),
        ("-H, --header", 'Specify custom HTTP headers in the format "Key: Value".'),
    ]
    for opt, desc in options:
        print(f"{opt.ljust(30)} {desc}")
    print("\n")