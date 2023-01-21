"""Used for doing various things with the Bottoken"""
import configparser
import json
import logging
import logging.config
import os

CONFIG_FILE_PATH = './config/main.cfg'
if os.path.exists(CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

logging.config.dictConfig(json.loads(open(config.get('Paths', 'logger_cfg-file_path'), 'r').read()))
logger = logging.getLogger(__name__)
logger.debug(': token_setup initialized')

def generate_token():
    gen_bool = str(input('Token Keyfile not found do you want to create one?[y/n]: '))
    if gen_bool == 'n' or gen_bool != 'y':
        os.exit()
    token = str(input('Enter Token: '))
    if token == '':
        os.exit()
    else:
        with open(str(config.get('Paths', 'token_file_path')), 'w') as token_file:
            token_file.write(token)
    logger.info('[Keyfile generator]: Token keyfile was created successfully')

def check_for_token():
    """Checks specified path for an token"""
    logger.debug('[Token Checker]: Checking for token keyfile')
    if not os.path.exists(config.get('Paths', 'token_file_path')):
        logger.warning('[Token Checker]: Keyfile not found!')
        generate_token()

    else:
        with open(config.get('Paths', 'token_file_path'), 'r') as token_file:
            token = token_file.readlines()
            logger.debug('[Token Checker]: Token keyfile loaded sucessfully')
        return token