import sys, os, asyncio
from colorama import init, Fore, Style
from modules.downloader import drm_downloader, validate_keys
from modules.logging import setup_logging
from modules.arg_parser import parse_arguments
from modules.proxy import init_proxy, proxyscrape, allowed_countries, rotate_proxy
from modules.pssh import get_pssh, amz_pssh, get_pssh_from_mpd, fetch_manifest_with_retry
from services.netflix import NetflixClient, download_netflix
from modules.utils import print_title, print_license_keys, clear_screen, colored_input
from modules.license_retrieval import get_license_keys

logging = setup_logging()

def main():
    init(autoreset=True)  # Ensure Colorama is initialized to auto-reset style after each print.
    clear_screen()  # Clear the console.

    try:
        args = parse_arguments()  # Parse CLI arguments.
    except Exception as e:
        logging.error(f"Error parsing arguments: {e}")
        sys.exit(1)

    print_title('Widevine-KSKEY', args.proxy)

    if args.service == "netflix":
        if not args.content_id:
            logging.error("Error: content_id is required for Netflix service.")
            sys.exit(1)
        asyncio.run(download_netflix(args.content_id, 'output'))
        return

    proxy = None
    if args.proxy:
        proxy_upper = args.proxy.upper()
        if proxy_upper in allowed_countries:
            proxy_data = {
                "zone": proxy_upper,
                "port": "peer"
            }
            proxy = init_proxy(proxy_data)
            proxy = {"http": proxy, "https": proxy}
        elif args.proxy.lower() == "scrape":
            proxies = proxyscrape()
            if proxies:
                proxy = {"http": proxies[0], "https": proxies[0]}
        elif args.proxy.lower() == "rotate":
            proxies = rotate_proxy()
            if proxies:
                proxy = {"http": proxies[0], "https": proxies[0]}
            else:
                logging.error("Failed to fetch proxies for rotation.")
                sys.exit(1)
        else:
            proxy = {"http": args.proxy, "https": args.proxy}

    if args.service == "prime" and args.mpd_url:
        pssh = amz_pssh(args.mpd_url, proxy)
    elif args.mpd_url:
        try:
            manifest = fetch_manifest_with_retry(args.mpd_url, proxy)
            pssh = get_pssh(args.mpd_url, proxy)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            pssh = None
    else:
        pssh = args.pssh

    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        sys.exit(1)

    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.mpd_url, proxy)
    
    if keys:
        print_license_keys(keys)
        print()
        proceed = colored_input(f"Continue with download? {Fore.RED}(Y/N): ", Fore.YELLOW).lower().strip()
        if proceed:
            print(Fore.MAGENTA + "=============================================================================================================")
        if proceed == 'n':
            logging.info("Download cancelled by the user.")
            sys.exit(0)
        elif proceed != 'y':
            logging.warning("Invalid input: Please enter Y for yes or N for no.")
            return

        save_name = colored_input("Enter the output name (Without Extension): ", Fore.CYAN).strip()
        if not save_name:
            logging.error("Invalid save name provided.")
            return

        if not args.mpd_url:
            logging.error("Invalid Manifest URL.")
            return

        validated_keys = validate_keys(keys)
        if not validated_keys:
            logging.error("No valid keys available to proceed with the download.")
            return

        service = args.service if args.service else colored_input("Enter the service name: ", Fore.CYAN).strip()
        successful = drm_downloader(args.mpd_url, save_name, validated_keys, output_format='mp4')
        
        if successful:
            logging.info("Content downloaded successfully.")
        else:
            logging.error("Content download failed.")
    else:
        logging.error("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()