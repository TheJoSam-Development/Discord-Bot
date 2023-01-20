import configparser
import discord
from discord.ext import bridge
import json
import logging
import logging.config
import os

from utils import token_setup

CONFIG_FILE_PATH = './config/main.cfg'
if os.path.exists(CONFIG_FILE_PATH):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

logging.config.dictConfig(json.loads(open(config.get('File Paths', 'logger_cfg-file_path'), 'r').read()))
logger = logging.getLogger(__name__)

# checks for token keyfile on specified path
TOKEN = str(list(token_setup.check_for_token())[0])

intents = discord.Intents.default()
intents.message_content = True


bot = bridge.Bot(command_prefix = config.get('Main Settings', 'command_prefix'), intents = intents)

@bot.command()
async def ping(ctx):
    await ctx.send('**PONG!**')

@bot.bridge_command()
async def ping2(ctx):
    await ctx.send('**PONG!** *Bridge*')

bot.run(TOKEN)