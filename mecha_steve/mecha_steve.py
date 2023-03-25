"""A Discord bot for playing music, and maybe other things"""
import logging
import asyncio
import discord
from help import MechaSteveHelp
from discord.ext import commands
from music.commands import Music

# Setting up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
dt_fmt = '%Y-%m-%d %H:%M:%S'
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
formatter = logging.Formatter('[{asctime}] [{levelname}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)


async def make_bot():
    intents = discord.Intents(messages=True, presences=True, guilds=True,
                              members=True, message_content=True, voice_states=True)
    bot = commands.Bot(command_prefix='$', intents=intents, help_command=MechaSteveHelp())
    await bot.add_cog(Music(bot, logger))
    return bot


with open('../token', encoding='utf-8') as f:
    token = f.read()

asyncio.run(make_bot()).run(token)
