import sys
import coloredlogs
import logging
from colorama import init, Fore, Style
from loguru import logger

def setup_logging():
    init(autoreset=True)

    logger_standard = logging.getLogger("Widevine-KSKEY")
    coloredlogs.install(level='DEBUG', logger=logger_standard, fmt='%(asctime)s - %(levelname)s - %(message)s')

    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>", level="DEBUG")
    logger.add("logs/logfile.log", rotation="5 MB", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}", level="DEBUG", encoding='utf8')
    return logger