import shutil, sys
from pathlib import Path
from typing import Optional
import pyfiglet
import importlib
from loguru import logger
from modules.pssh import get_pssh

def get_binary_path(*names: str) -> Optional[Path]:
    """Get the path of the first found binary name."""
    for name in names:
        path = shutil.which(name)
        if path:
            return Path(path)
    return None

def print_title(title_text, proxy=None):
    title = pyfiglet.figlet_format(title_text, font='slant')
    logger.debug(title)
    if proxy:
        logger.debug(f"Proxy: {proxy}")

def generate_pssh(mpd_url):
    return get_pssh(mpd_url)

def print_license_keys(keys):
    for key in keys:
        logger.info(key)
    logger.success("All Done...")

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logger.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)