import sys, os, asyncio
from colorama import init, Fore, Style
from modules.downloader import drm_downloader, validate_keys
from modules.logging import setup_logging
from modules.arg_parser import parse_arguments
from modules.pssh import get_pssh, amz_pssh
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
        print(f"{Fore.RED}Error parsing arguments: {e}{Style.RESET_ALL}")
        sys.exit(1)

    print_title('Widevine-KSKEY', args.proxy)

    if args.service == "netflix":
        if not args.content_id:
            print(f"{Fore.RED}Error: content_id is required for Netflix service.{Style.RESET_ALL}")
            sys.exit(1)
        asyncio.run(download_netflix(args.content_id, 'output'))
        return
    
    if args.service == "prime" and args.mpd_url:
        pssh = amz_pssh(args.mpd_url)
    elif args.mpd_url:
        pssh = get_pssh(args.mpd_url)
    else:
        pssh = args.pssh

    if not pssh:
        logging.error("No PSSH data provided or extracted.")
        sys.exit(1)

    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.mpd_url, proxy)
    if keys:
        print_license_keys(keys)
        print()
        proceed = colored_input("Continue with download? (Y/N): ", Fore.YELLOW).lower().strip()
        if proceed == 'n':
            logging.info("Download cancelled by the user.")
            sys.exit(0)
        elif proceed != 'y':
            logging.warning("Invalid input: Please enter Y for yes or N for no.")
            return

        args.mpd_url = colored_input("Enter Manifest URL: ", Fore.YELLOW)
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