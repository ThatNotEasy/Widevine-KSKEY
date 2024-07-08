import sys
import os
import asyncio
from colorama import init, Fore, Style
from modules.downloader import drm_downloader, validate_keys, fetch_mpd, parse_mpd, display_tracks, yt_dlp_downloader
from modules.logging import setup_logging
from modules.config import load_configurations
from modules.arg_parser import parse_arguments
from modules.proxy import init_proxy, proxyscrape, allowed_countries, rotate_proxy
from modules.pssh import get_pssh, amz_pssh, get_pssh_from_mpd, fetch_manifest_with_retry, fetch_m3u8, extract_pssh_from_m3u8
from services.netflix import NetflixClient, download_netflix
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

    # Handling for specific service types with additional checks
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
    if args.proxy:
        proxy_upper = args.proxy.upper()
        if proxy_upper in allowed_countries:
            proxy_data = init_proxy({"zone": proxy_upper, "port": "peer"})
            proxy = {"http": proxy_data, "https": proxy_data}
        elif args.proxy.lower() == "scrape":
            proxy = proxyscrape()
        elif args.proxy.lower() == "rotate":
            proxy = rotate_proxy()
        else:
            proxy = {"http": args.proxy, "https": args.proxy}
    return proxy

def get_pssh_data(args, proxy):
    # logging.debug(f"Using proxy: {proxy}")
    if args.service == "prime" and args.mpd_url:
        return amz_pssh(args.mpd_url, proxy)
    elif args.mpd_url:
        try:
            manifest = fetch_manifest_with_retry(args.mpd_url, proxy)
            return get_pssh(args.mpd_url, proxy)
        except Exception as e:
            logging.error(f"An error occurred fetching PSSH data: {e}")
            return None
    elif args.mpd_url:
        try:
            return extract_pssh_from_m3u8(args.mpd_url)
        except Exception as e:
            logging.error(f"An error occurred extracting PSSH from M3U8: {e}")
            return None
    else:
        return args.pssh

def proceed_with_download(args, keys, proxy):
    print_license_keys(keys)
    if confirm_user_proceed():
        logging.info(f"Download options: {Fore.RED}[1] {Fore.GREEN}N3MU8DL (Recommended) {Fore.YELLOW}| {Fore.RED}[2] {Fore.GREEN}YT-DLP{Fore.RESET}")
        print(Fore.MAGENTA + "=============================================================================================================")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == '1':
            save_name = colored_input("Enter the output name (WithoutExtension): ", Fore.CYAN).strip()
            if not save_name:
                logging.error("Invalid save name provided.")
                return

            mpd_content = fetch_mpd(args.mpd_url, proxy)
            if not mpd_content:
                logging.error("Failed to fetch MPD content.")
                return
            
            validated_keys = validate_keys(keys)
            if validated_keys:
                successful = drm_downloader(args.mpd_url, save_name, validated_keys, output_format='mkv')
                if successful:
                    logging.info("Content downloaded successfully.")
                else:
                    logging.error("Content download failed.")
            else:
                logging.error("No valid keys available to proceed with the download.")
        
        elif choice == '2':
            video_info = yt_dlp_downloader(args.mpd_url, 2, 'best')
            if 'error' in video_info:
                logging.error("Failed to fetch video info: " + video_info['error'])
            else:
                print(video_info)

def confirm_user_proceed():
    init(autoreset=True)
    proceed = colored_input(f"Continue with download? {Fore.RED}(Y/N): ", Fore.YELLOW).lower().strip()
    print(Fore.MAGENTA + "=============================================================================================================")
    if proceed == 'n':
        logging.info("Download cancelled by the user.")
        return False
    elif proceed == 'y':
        return True
    else:
        logging.warning("Invalid input: Please enter Y for yes or N for no.")
        return False

if __name__ == "__main__":
    main()