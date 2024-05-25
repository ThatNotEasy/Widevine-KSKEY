import shutil, sys
from pathlib import Path
from typing import Optional
import pyfiglet
from colorama import Fore, Style
import importlib
from modules.initialization import initialize

session, logging = initialize()

def get_binary_path(*names: str) -> Optional[Path]:
    """Get the path of the first found binary name."""
    for name in names:
        path = shutil.which(name)
        if path:
            return Path(path)
    return None

def print_title(title_text, proxy=None):
    title = pyfiglet.figlet_format(title_text, font='slant')
    if proxy:
        print(Fore.YELLOW + f"{title}Running with proxy settings: {proxy}" + Style.RESET_ALL)
    else:
        print(Fore.CYAN + f"{title}Running " + Style.RESET_ALL)

def print_license_keys(keys):
    for key in keys:
        logging.info(key)
    logging.success("All Done...")

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logging.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)