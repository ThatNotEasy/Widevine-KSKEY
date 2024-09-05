import sys
import asyncio
from colorama import init, Fore
from modules.downloader import drm_downloader, validate_keys, fetch_mpd, direct_downloads
from modules.logging import setup_logging
from modules.config import load_configurations
from modules.arg_parser import parse_arguments
from services.netflix import download_netflix
from modules.proxy import init_proxy, proxyscrape, allowed_countries, rotate_proxy
from modules.pssh import amz_pssh, extract_pssh_from_m3u8, fetch_manifest, extract_kid_and_pssh_from_mpd, pssh_parser
from modules.utils import print_title, print_license_keys, clear_screen, colored_input, parse_headers
from modules.license_retrieval import get_license_keys

logging = setup_logging()
config = load_configurations()

def main():
    init(autoreset=True)
    clear_screen()
    print_title('Widevine-KSKEY')
    args = parse_arguments()

    headers = parse_headers(args.header)
    
    if args.downloads and args.mpd_url:
        proxy = args.proxy if args.proxy else None
        output_name = args.output if args.output else "default"
        direct_downloads(args.mpd_url, output_name, proxy)
    else:
        logging.info("You must provide both -d (downloads) and -m (MPD URL) to trigger the download.")
        print(Fore.MAGENTA + "=" * 120)

    if not args.service:
        logging.error("No service specified. Please specify a service to proceed.")
        sys.exit(1)

    if args.service.lower() == "netflix":
        handle_netflix(args)
    else:
        handle_other_services(args, headers)

def handle_netflix(args):
    if not args.content_id:
        logging.error("Error: content_id is required for Netflix service.")
        sys.exit(1)
    asyncio.run(download_netflix(args.content_id, 'output'))

def handle_other_services(args, headers):
    proxy = setup_proxy(args)
    pssh = get_pssh_data(args, proxy)
    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        sys.exit(1)

    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.mpd_url, proxy)
    
    if keys:
        proceed_with_download(args, keys, proxy, headers)
    else:
        logging.error("Failed to retrieve valid keys.")

def setup_proxy(args):
    proxy = {}
    proxy_input = args.proxy.lower() if args.proxy else ""
    
    if proxy_input == "scrape":
        logging.info("Using 'scrape' proxy method.")
        proxy = proxyscrape()
        
    elif proxy_input == "rotate":
        logging.info("Using 'rotate' proxy method.")
        print(Fore.MAGENTA + "=" * 120)
        proxy = rotate_proxy()
        
    elif proxy_input.upper() in allowed_countries:
        logging.info(f"Using country-based proxy for: {proxy_input.upper()}.")
        print(Fore.MAGENTA + "=" * 120)
        proxy_data = init_proxy({"zone": proxy_input.upper(), "port": "peer"})
        proxy = {"http": proxy_data, "https": proxy_data}
        
    else:
        if args.proxy:
            logging.info(f"Using provided proxy: {args.proxy}")
            print(Fore.MAGENTA + "=" * 120)
            proxy = {"http": args.proxy, "https": args.proxy}
        else:
            pass
            # logging.info("No proxy provided. Continuing without a proxy.")
    return proxy

def get_pssh_data(args, proxy):
    try:
        if args.service == "prime" and args.mpd_url:
            return amz_pssh(args.mpd_url, proxy)
        elif args.mpd_url:
            # Parse headers only if provided, fetch manifest, and extract KID and PSSH
            parsed_headers = parse_headers(args.header) if args.header else None
            manifest = fetch_manifest(args.mpd_url, proxy, parsed_headers)
            return extract_kid_and_pssh_from_mpd(manifest) if manifest else None
        elif args.pssh:
            return pssh_parser(args.pssh)
        else:
            return None
    except Exception as e:
        logging.error(f"An error occurred fetching PSSH data: {e}")
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

            mpd_url = args.mpd_url or input(f"{Fore.GREEN}Enter Manifest URL: {Fore.WHITE}{Fore.RESET}").strip()
            if not mpd_url:
                logging.error("No manifest URL provided.")
                return

            mpd_content = fetch_mpd(mpd_url, proxy, headers)
            if not mpd_content:
                logging.error("Failed to fetch MPD content.")
                return
            
            for key in keys:
                validated_key = validate_keys(key)
                if validated_key:
                    drm_downloader(mpd_url, save_name, validated_key, proxy)
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
