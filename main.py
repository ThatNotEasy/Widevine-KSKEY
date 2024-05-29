import sys, os
from colorama import init, Fore, Style
from modules.downloader import drm_downloader, validate_keys
from modules.initialization import initialize
from modules.arg_parser import parse_arguments
from modules.pssh import get_pssh
from modules.utils import print_title, print_license_keys
from modules.license_retrieval import get_license_keys

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_input(prompt, color):
    """Function to print a prompt in a specific color and return the user input."""
    print(color + prompt + Style.RESET_ALL, end='')
    return input()


def main():
    init(autoreset=True)  # Ensure Colorama is initialized to auto-reset style after each print.
    clear_screen()  # This function needs to be defined to clear the console.

    try:
        args = parse_arguments()  # Ensure this function is implemented to parse CLI arguments.
    except Exception as e:
        print(f"{Fore.RED}Error parsing arguments: {e}{Style.RESET_ALL}")
        sys.exit(1)

    session, logger = initialize()  # Make sure initialize function returns a session object and a logger.
    print_title('Widevine-KSKEY', args.proxy)  # Define or import print_title function.

    pssh = args.pssh or (get_pssh(args.mpd_url) if args.mpd_url else None)
    if not pssh:
        logger.error("No PSSH data provided or extracted.")
        sys.exit(1)

    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    keys = get_license_keys(pssh, args.license_url, args.service, args.content_id or args.mpd_url, proxy)
    if keys:
        print_license_keys(keys)
        print()
        proceed = colored_input("Continue with download? (Y/N): ", Fore.YELLOW).lower().strip()
        if proceed == 'n':
            logger.info("Download cancelled by the user.")
            sys.exit(0)
        elif proceed != 'y':
            logger.warning("Invalid input: Please enter Y for yes or N for no.")
            return

        args.mpd_url = colored_input("Enter Manifest URL: ", Fore.YELLOW)
        save_name = colored_input("Enter the output name (Without Extension): ", Fore.CYAN).strip()
        if not save_name:
            logger.error("Invalid save name provided.")
            return

        if not args.mpd_url:
            logger.error("Invalid Manifest URL.")
            return

        validated_keys = validate_keys(keys)
        if not validated_keys:
            logger.error("No valid keys available to proceed with the download.")
            return

        service = args.service if args.service else colored_input("Enter the service name: ", Fore.CYAN).strip()
        successful = drm_downloader(args.mpd_url, save_name, validated_keys, output_format='mp4')
        if successful:
            logger.info("Content downloaded successfully.")
        else:
            logger.error("Content download failed.")
    else:
        logger.error("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()