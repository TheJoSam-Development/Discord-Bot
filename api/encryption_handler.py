"""
This is an Module which focuses on making encrypt and decrypt calls consistent
This Feature is currently not available!
"""

import configparser
import logging
from os import path

PATH_CONFIG = './config/paths.cfg'
if path.exists(PATH_CONFIG):
    paths = configparser.ConfigParser()
    paths.read(PATH_CONFIG)
else: raise FileNotFoundError(f'File {PATH_CONFIG} not found!')

CONFIG_PATH = paths.get(section='Config Files', option='encryption_config')
if path.exists(CONFIG_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
else: raise FileNotFoundError(f'File {CONFIG_PATH} not found!')

LOGGER_CONFIG_FILE = paths.get(section='Log Paths', option='logger_cfg_file')
if path.exists(LOGGER_CONFIG_FILE):
    logging.config.dictConfig(
    json.loads(open(LOGGER_CONFIG_FILE, 'r').read()))
    logger = logging.getLogger(__name__)
else: raise FileNotFoundError(f'File {LOGGER_CONFIG_FILE} not found!')

