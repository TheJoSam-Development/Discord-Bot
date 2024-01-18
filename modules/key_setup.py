"""
This Module includes all needed features to initiate an keycheck and request an input
Also usable for all key systems but primarly used for Bot internal Keys
"""
import os
import configparser
import logging
import logging.config
import json
import csv
from cryptography.fernet import Fernet

from modules import uuid_generator

# Path to main config
CONFIG_FILE_PATH = './config/main.cfg'

if os.path.exists(CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
else: raise FileNotFoundError(f'File {CONFIG_FILE_PATH} not found!')

logging.config.dictConfig(
    json.loads(open(config.get(section='Paths', option='logger_cfg_file'), 'r').read()))
logger = logging.getLogger(__name__)
logger.info('Key Tools initiated')

if config.getboolean(section='Key_system', option='encryption'):
    logger.info('Encryption enabled')
    if os.path.exists(config.get(section='Key_system', option='encryption_key')):
        with open(config.get(section='Key_system', option='encryption_key'), 'rb') as key_file:
            encryption = Fernet(key=key_file.read())
            logger.debug('Initialized encryption key')
    else:
        with open(config.get(section='Key_system', option='encryption_key'), 'wb') as key_file:
            key = Fernet.generate_key()
            key_file.write(key)
            encryption = Fernet(key)
            logger.debug('Generated encryption key')
else:
    logger.warning('Encryption is disabled! This is NOT recommended!')

def generate_key(path: str, key_content: str, author: str, key_hash: str = '##NO#HASH##'):
    tuid = uuid_generator.generate(type=1)
    if config.getboolean(section='Key_system', option='append_tuid'):
        key_file = open((path + tuid), 'w')
    else: key_file = open(path, 'w')
    _key_template_file = open(config.get(section='Paths', option='key_template'), 'r').read()
    key_template = json.loads(_key_template_file)
    key_template['author'] = author
    key_template['tuid']   = tuid
    if config.getboolean(section='Key_system', option='encryption'):
        key_template['key']  = str(encryption.encrypt(key_content.encode()))
        key_template['hash'] = str(encryption.encrypt(key_hash.encode()))
    else:
        key_template['key']  = key_content
        key_template['hash'] = key_hash
    json.dump(key_template, key_file, indent=4)
    logger.debug(f'Key Generator finished key: {path}')

def register_key(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError('Keyfile not found')
    key_author = json.loads(open(path, 'r').read())['author']
    key_tuid   = json.loads(open(path, 'r').read())['tuid']
    if config.get(section='Key_system', option='key_register_type') == 'CSV':
        if os.path.exists(config.get(section='Paths', option='key_register')):
            with open(config.get(section='Paths', option='key_register'), 'a') as register:
                fieldnames = ['Key Path', 'Author', 'TUID']
                writer = csv.DictWriter(register, fieldnames=fieldnames)
                writer.writerow({'Author':key_author, 'Key Path':path, 'TUID':key_tuid})
        else:
            with open(config.get(section='Paths', option='key_register'), 'w') as register:
                fieldnames = ['Key Path', 'Author', 'TUID']
                writer = csv.DictWriter(register, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Author':key_author, 'Key Path':path, 'TUID':key_tuid})