import sys
import asyncio
import requests
from colorama import init, Fore
from modules.downloader import drm_downloader, validate_keys, fetch_mpd, direct_downloads
from modules.logging import setup_logging
from modules.config import load_configurations
from modules.arg_parser import parse_arguments
from modules.proxy import init_proxy, proxyscrape, allowed_countries, rotate_proxy, used_proxy, read_proxies_from_file
from modules.pssh import fetch_manifest, get_pssh_from_m3u8_url, pssh_parser, extract_kid_and_pssh_from_mpd, kid_to_pssh
from modules.utils import print_title, print_license_keys, clear_screen, colored_input, parse_headers, extract_widevine_pssh, bypass_manifest_fetching
from modules.license_retrieval import get_license_keys, configure_session

logging = setup_logging()
config = load_configurations()

def setup_proxy(args):
    proxies = []
    proxy_method = args.proxy.lower() if args.proxy else ""
    country_code = args.country_code.upper() if args.country_code else None

    if proxy_method == "file":
        proxies = read_proxies_from_file('proxies.txt')
        if not proxies:
            logging.warning("No proxies found in the file.")
            return {}

    elif proxy_method == "scrape":
        if country_code in allowed_countries:
            logging.info(f"{Fore.YELLOW}Using {Fore.GREEN}scrape {Fore.YELLOW}proxy method for country: {Fore.GREEN}{country_code}.{Fore.RESET}")
            print(Fore.MAGENTA + "=" * 120)
            proxy_url = proxyscrape(country_code)
            if proxy_url:
                proxies.append(proxy_url)
            else:
                logging.warning(f"No proxies found for country: {country_code}.")
        else:
            logging.info("Using 'scrape' proxy method with no specific country code.")
            proxy_url = proxyscrape()
            if proxy_url:
                proxies.append(proxy_url)
            else:
                logging.warning("No proxies found.")

    elif proxy_method == "rotate":
        logging.info("Using 'rotate' proxy method.")
        proxy = rotate_proxy()
        proxies.append(proxy)

    elif proxy_method.upper() in allowed_countries:
        logging.info(f"Using country-based proxy for: {proxy_method.upper()}.")
        proxy_data = init_proxy({"zone": proxy_method.upper(), "port": "peer"})
        proxies.append(proxy_data)

    else:
        if args.proxy:
            logging.info(f"{Fore.YELLOW}Using provided proxy: {Fore.GREEN}{args.proxy}{Fore.RESET}")
            print(Fore.MAGENTA + "=" * 120)
            proxy_url = args.proxy
            proxies.append(used_proxy(proxy_url) if proxy_url.startswith('socks') else used_proxy({'http': proxy_url, 'https': proxy_url}))

    working_proxies = {}
    for proxy in proxies:
        test_proxy = used_proxy(proxy)
        logging.info(f"Testing proxy: {test_proxy}")
        print(Fore.MAGENTA + "=" * 120)
        if not test_proxy:
            logging.warning(f"Invalid proxy format: {proxy}")
            continue
        
        session = configure_session(test_proxy)
        try:
            response = session.get('https://httpbin.org/ip', timeout=5)
            if response.status_code == 200:
                logging.info(f"Working proxy found: {test_proxy}")
                working_proxies = test_proxy
                break  # Exit the loop if a working proxy is found
        except requests.RequestException as e:
            logging.error("No working proxies found.")
            print(Fore.MAGENTA + "=" * 120)
            continue
            
    if not working_proxies:
        pass
    return working_proxies


def main():
    init(autoreset=True)
    clear_screen()
    print_title('Widevine-KSKEY')
    args = parse_arguments()

    headers = parse_headers(args.header)
    
    if args.downloads and args.manifest_url:
        proxy = setup_proxy(args)
        output_name = args.output if args.output else "default"
        direct_downloads(args.manifest_url, output_name, proxy)
    else:
        print(f"{Fore.RED}Disclaimer: {Fore.WHITE}You must provide both {Fore.GREEN}'-d --downloads {Fore.RED}& {Fore.GREEN}-m --manifest-url' {Fore.WHITE}to trigger the download. (HLS ONLY){Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120 + "\n")

    if not args.service:
        logging.error("No service specified. Please specify a service to proceed.")
        sys.exit(1)
    else:
        handle_other_services(args, headers)

def handle_other_services(args, headers):
    proxy = setup_proxy(args)
    pssh = get_pssh_data(args, proxy)
    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        sys.exit(1)

    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.manifest_url, proxy)
    
    if keys:
        proceed_with_download(args, keys, proxy, headers)
    else:
        pass

def get_pssh_data(args, proxy):
    if args.pssh:
        return pssh_parser(args.pssh)
    
    if args.kid:
        logging.info(f"{Fore.YELLOW}KEYID (KID): {Fore.GREEN}{args.kid}{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120)
        pssh = kid_to_pssh(args.kid)
        if pssh:
            return pssh
        else:
            logging.error("Failed to convert KID to PSSH.")
            return None

    if not args.manifest_url:
        logging.warning("No manifest URL provided.")
        return None

    manifest = fetch_manifest(args.manifest_url, proxy)
    if not manifest:
        logging.error("Failed to fetch manifest.")
        return None

    if '.mpd' in args.manifest_url:
        pssh = extract_kid_and_pssh_from_mpd(manifest)
        if pssh:
            return pssh
        pssh = bypass_manifest_fetching(args.manifest_url)
        if pssh:
            return extract_widevine_pssh()
    
    if '.m3u8' in args.manifest_url:
        return get_pssh_from_m3u8_url(args.manifest_url)
    
    logging.warning("Unsupported manifest URL type.")
    return None

def proceed_with_download(args, keys, proxy, headers):
    print_license_keys(keys)
    if confirm_user_proceed():
        logging.info(f"Download options: {Fore.RED}[1] {Fore.GREEN}N3MU8DL (Recommended) {Fore.YELLOW}| {Fore.RED}[2] {Fore.GREEN}YT-DLP{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 120)
        choice = input("Enter your choice (1 or 2): ").strip()
        print(Fore.MAGENTA + "=" * 120)

        if choice == '1':
            save_name = colored_input("Enter the output name (WithoutExtension): ", Fore.CYAN).strip()
            if not save_name:
                logging.error("Invalid save name provided.")
                return

            manifest_url = args.manifest_url or input(f"{Fore.GREEN}Enter Manifest URL: {Fore.WHITE}{Fore.RESET}").strip()
            if not manifest_url:
                logging.error("No manifest URL provided.")
                return

            mpd_content = fetch_mpd(manifest_url, proxy, headers)
            if not mpd_content:
                logging.error("Failed to fetch MPD content.")
                return
            
            for key in keys:
                validated_key = validate_keys(key)
                if validated_key:
                    drm_downloader(manifest_url, save_name, validated_key, proxy)
                else:
                    logging.error("Invalid key: %s", key)
        
        elif choice == '2':
            logging.info(f"{Fore.RED}Under Construction!")
            # Implement YT-DLP download logic here when ready.

def confirm_user_proceed():
    proceed = colored_input(f"Continue with download? {Fore.RED}(Y/N): ", Fore.YELLOW).lower().strip()
    print(Fore.MAGENTA + "=" * 108)
    if proceed == 'y':
        return True
    elif proceed == 'n':
        logging.info("Download cancelled by the user.")
        return False
    else:
        logging.warning("Invalid input: Please enter Y for yes or N for no.")
        return False

if __name__ == "__main__":
    main()