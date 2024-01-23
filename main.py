import configparser
import discord
from discord.ext import bridge
import json
import logging
import logging.config
from os import path

CONFIG_FILE_PATH = './config/main.cfg'

if __name__ != '__main__': raise RuntimeError('Main.py cannot be imported or run as subprocess')

if path.exists(CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

logging.config.dictConfig(
    json.loads(open(config.get(section='Paths', option='logger_cfg_file'), 'r').read())
    )
logger = logging.getLogger(__name__)

if path.exists(config.get(section='Main', option='key_file')):
    token = open(
        file=config.get(section='Main', option='key_file'),
        mode='r').readlines()[0]
    logger.info('Keyfile found and loaded')

intents = discord.Intents.all()

bot = bridge.Bot(command_prefix=config.get(section='Main', option='prefix'), intents=intents)
bot.run(token)