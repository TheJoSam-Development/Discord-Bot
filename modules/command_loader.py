import configparser
import discord
from discord.ext import bridge
import os
import datetime

import config_loader
config = config_loader.get_config(cfg_name = 'commands')

def scan_commands_dir():
    commands_dir = os.listdir(config.get('Main', 'commands_dir'))
    command_list = []
    for command in commands_dir:
        if command.endswith('.py'):
            command_list.append('commands.' + command[:-3])
    return command_list