import sys
import requests
import coloredlogs
from colorama import init
from loguru import logger

def initialize():
    init(autoreset=True)
    session = requests.Session()
    coloredlogs.install(level='DEBUG')
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", level="DEBUG")
