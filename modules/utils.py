import shutil, sys, os
from pathlib import Path
from typing import Optional
import pyfiglet
from colorama import Fore, Style
import importlib
from modules.logging import setup_logging
import requests, random, os, re, time
from lxml import html, etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from bs4 import BeautifulSoup
from http.cookiejar import MozillaCookieJar

logging = setup_logging()

def bypass_manifest_fetching(url: str) -> Optional[str]:
    chrome_driver_path = 'modules/chromedriver.exe'
    extension_path = 'modules/manifest_viewer.crx'
    
    chrome_options = Options()
    if os.path.exists(extension_path):
        chrome_options.add_extension(extension_path)
    else:
        logging.warning(f"Extension file not found at {extension_path}. Skipping extension loading.")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)  # Adjust sleep time if necessary

    manifest_content = driver.page_source
    if not manifest_content:
        logging.error("No content found on manifest page.")
        return None

        # Parse the HTML and extract the <body> content
    tree = html.fromstring(manifest_content)
    body_content = tree.xpath('//body')[0].text_content()

    manifest_file_path = "logs/manifest.mpd"
    os.makedirs('logs', exist_ok=True)
    with open(manifest_file_path, "w", encoding="utf-8") as file:
        file.write(body_content)
        
    logging.info(f"{Fore.YELLOW}Success - {Fore.GREEN}[200]: Manifest has been bypassed!{Fore.RESET}")
    print(Fore.MAGENTA + "=" * 120)

    return body_content
        
def extract_widevine_pssh() -> str:
    manifest_file_path = 'logs/manifest.mpd'
    
    if not os.path.exists(manifest_file_path):
        logging.error(f"Manifest file not found at {manifest_file_path}.")
        return None

    with open(manifest_file_path, "r", encoding="utf-8") as file:
        content = file.read()
        
    tree = etree.HTML(content)

    nsmap = {'cenc': 'urn:mpeg:cenc:2013'}
    cp_elements = tree.xpath('//ContentProtection', namespaces={'': 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed'})
    if not cp_elements:
        logging.error("No ContentProtection elements found in the manifest.")
        return None
    
    # Extract PSSH data
    for cp in cp_elements:
        scheme_id_uri = cp.get('schemeIdUri')
        if scheme_id_uri == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
            pssh_elements = cp.xpath('.//cenc:pssh', namespaces=nsmap)
            if not pssh_elements:
                logging.error("No pssh elements found in ContentProtection.")
                return None
            
            for pssh in pssh_elements:
                pssh_data = pssh.text
                if not pssh_data:
                    logging.error("No PSSH data found in pssh element.")
                    return None
                
                logging.info(f"PSSH Data: {pssh_data}")
                return pssh_data

        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_headers(header_list):
    """
    Convert a list of header strings into a dictionary.

    Args:
        header_list (list): List of headers in the format "Key: Value".

    Returns:
        dict: Dictionary of headers.
    """
    headers = {}
    if header_list:
        for header in header_list:
            if ':' in header:
                try:
                    key, value = header.split(":", 1)
                    headers[key.strip()] = value.strip()
                except ValueError as e:
                    logging.warning(f"Failed to process header: {header} due to {str(e)}.")
            else:
                pass
    return headers

def colored_input(prompt, color):
    print(color + prompt + Style.RESET_ALL, end='')
    return input()

def get_binary_path(*names: str) -> Optional[Path]:
    """Get the path of the first found binary name."""
    for name in names:
        path = shutil.which(name)
        if path:
            return Path(path)
    return None

def print_title(title_text):
    title = pyfiglet.figlet_format(title_text, font='slant')
    print(Fore.CYAN + f"{title}Running " + Style.RESET_ALL)

def print_license_keys(keys):
    for key in keys:
        logging.info(key)
    print(Fore.MAGENTA + "=============================================================================================================")
    logging.success("All Done...\n")

def get_service_module(service_name):
    try:
        return importlib.import_module(f'services.{service_name}')
    except ImportError:
        logging.error(f"No module named '{service_name}' found in 'services' package")
        sys.exit(1)