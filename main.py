import sys, os
from modules.initialization import initialize
from modules.arg_parser import parse_arguments
from modules.utils import print_title, generate_pssh, print_license_keys
from modules.license_retrieval import get_license_keys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    args = parse_arguments()
    initialize()
    print_title('\n' + 'Widevine-KSKEY', args.proxy)
    
    lic_url = args.license_url
    pssh = args.pssh or (generate_pssh(args.mpd_url) if args.mpd_url else None)

    if not pssh and args.service != "hbogo":
        logger.error("No PSSH data provided or extracted.")
        return
    
    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    
    keys = get_license_keys(pssh, lic_url, args.service, args.content_id, proxy)
    if keys:
        print_license_keys(keys)
    else:
        logger.error("Failed to retrieve valid keys.")

if __name__ == "__main__":
    main()