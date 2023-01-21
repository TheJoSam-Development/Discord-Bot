import configparser
import discord
from discord.ext import bridge
import json
import logging
import logging.config
import os

from modules import token_setup
from modules import command_loader

CONFIG_FILE_PATH = './config/main.cfg'
EXTENSIONS = []

if os.path.exists(CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

logging.config.dictConfig(json.loads(open(config.get('Paths', 'logger_cfg-file_path'), 'r').read()))
logger = logging.getLogger(__name__)

# checks for token keyfile on specified path
TOKEN = str(list(token_setup.check_for_token())[0])

intents = discord.Intents.default()
intents.message_content = True


bot = bridge.Bot(command_prefix = config.get('Main Settings', 'command_prefix'), intents = intents)
#bot.remove_command('help')

if EXTENSIONS != []:
    for extension in EXTENSIONS:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.error(f'Failed to load extension: {extension}')
            logger.error(e)

command_list = command_loader.scan_commands_dir()
if command_list != []:
    for command in command_list:
        try:
            bot.load_extension(command)
        except Exception as e:
            logger.error(f'Failed to load command: {command}')
            logger.error(e)

@bot.command()
async def ping(ctx):
    await ctx.send('**PONG!**')

@bot.slash_command()
async def ping(ctx):
    await ctx.send('**PONG!** *Slash*')

@bot.bridge_command()
async def ping2(ctx):
    await ctx.send('**PONG!** *Bridge*')

bot.run(TOKEN)