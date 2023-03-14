import discord
from discord.ext import bridge
import os
import datetime
import json

from modules import config_loader
config = config_loader.get_config(cfg_name = 'commands')

def scan_dir():
    """
    Scans in commands and meta dir for files

    Returns:
        command_list[list]: returns an list in pycord format for loading commands
        meta_list[list]: return an list similar to the command_list but with meta files
    """
    commands_dir = os.listdir(config.get('Main', 'commands_dir'))
    meta_dir = os.listdir(config.get('Main', 'commands_dir') + 'meta/')
    command_list = []
    meta_list = []
    for command in commands_dir:
        if command.endswith('.py'):
            command_list.append('commands.' + command[:-3])
    for meta_file in meta_dir:
        if meta_file.endswith('.cmdmeta'):
            meta_list.append(f'meta.{meta_file[:-8]}')
    return command_list, meta_list


def load_commands(bot, command_list: list, meta_file_list: list):
    """
    Loads all commands that are in the Commands Folder and combine them with their metas
    
    Args:
        bot: Discord Bot instance
    """
    for command in command_list:
        bot.load_extension(command)
        print('Loaded ' + command)


if __name__ == '__main__':
    print(scan_dir())
