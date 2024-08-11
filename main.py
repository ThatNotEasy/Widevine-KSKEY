import sys
import asyncio
from colorama import init, Fore
from modules.downloader import drm_downloader, validate_keys, fetch_mpd
from modules.logging import setup_logging
from modules.config import load_configurations
from modules.arg_parser import parse_arguments
from services.netflix import download_netflix
from modules.proxy import init_proxy, proxyscrape, allowed_countries, rotate_proxy
from modules.pssh import amz_pssh, extract_pssh_from_m3u8, fetch_manifest, extract_kid_and_pssh_from_mpd, pssh_parser
from modules.utils import print_title, print_license_keys, clear_screen, colored_input
from modules.license_retrieval import get_license_keys

logging = setup_logging()
config = load_configurations()

def main():
    init(autoreset=True)
    clear_screen()
    print_title('Widevine-KSKEY')
    args = parse_arguments()

    if not args.service:
        logging.error("No service specified. Please specify a service to proceed.")
        sys.exit(1)

    if args.service.lower() == "netflix":
        handle_netflix(args)
    else:
        handle_other_services(args)

def handle_netflix(args):
    if not args.content_id:
        logging.error("Error: content_id is required for Netflix service.")
        sys.exit(1)
    asyncio.run(download_netflix(args.content_id, 'output'))

def handle_other_services(args):
    proxy = setup_proxy(args)
    pssh = get_pssh_data(args, proxy)
    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        sys.exit(1)

    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.mpd_url, proxy)
    
    if keys:
        proceed_with_download(args, keys, proxy)
    else:
        logging.error("Failed to retrieve valid keys.")

def setup_proxy(args):
    proxy = {}
    proxy_input = args.proxy.lower() if args.proxy else ""
    
    if proxy_input == "scrape":
        proxy = proxyscrape()
    elif proxy_input == "rotate":
        proxy = rotate_proxy()
    elif proxy_input.upper() in allowed_countries:
        proxy_data = init_proxy({"zone": proxy_input.upper(), "port": "peer"})
        proxy = {"http": proxy_data, "https": proxy_data}
    else:
        proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else {}
    
    return proxy

def get_pssh_data(args, proxy):
    try:
        if args.service == "prime" and args.mpd_url:
            return amz_pssh(args.mpd_url, proxy)
        elif args.mpd_url:
            manifest = fetch_manifest(args.mpd_url, proxy)
            return extract_kid_and_pssh_from_mpd(manifest) if manifest else None
        elif args.pssh:
            return pssh_parser(args.pssh)
        else:
            return None
    except Exception as e:
        logging.error(f"An error occurred fetching PSSH data: {e}")
        return None

def proceed_with_download(args, keys, proxy):
    print_license_keys(keys)
    if confirm_user_proceed():
        logging.info(f"Download options: {Fore.RED}[1] {Fore.GREEN}N3MU8DL (Recommended) {Fore.YELLOW}| {Fore.RED}[2] {Fore.GREEN}YT-DLP{Fore.RESET}")
        print(Fore.MAGENTA + "=" * 108)
        choice = input("Enter your choice (1 or 2): ").strip()
        print(Fore.MAGENTA + "=" * 108)

        if choice == '1':
            save_name = colored_input("Enter the output name (WithoutExtension): ", Fore.CYAN).strip()
            if not save_name:
                logging.error("Invalid save name provided.")
                return

            mpd_url = args.mpd_url or input(f"{Fore.GREEN}Enter Manifest URL: {Fore.WHITE}{Fore.RESET}").strip()
            if not mpd_url:
                logging.error("No manifest URL provided.")
                return

            mpd_content = fetch_mpd(mpd_url, proxy)
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
