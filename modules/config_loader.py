import configparser
import os

CONFIG_DIRECTORY = './config/'


def get_config(cfg_name: str):
    _config_file_path = CONFIG_DIRECTORY + cfg_name + '.cfg'

    if os.path.exists(_config_file_path):
        config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
        config.read(_config_file_path)

    return config