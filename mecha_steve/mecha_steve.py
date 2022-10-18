"""A Discord bot for playing music, and maybe other things"""
import logging
import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('$(asctime)s:#(levelname)s:%(name)s: %message)s'))

intents = discord.Intents(messages=True, presences=True, guilds=True,
                          members=True,  message_content=True, voice_states=True)

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command(invoke_without_subcommand=True)
async def join(ctx):
    """Joins the voice channel the user who send the command is in"""
    print(ctx.author.voice)
    if ctx.author.voice is None:
        return await ctx.send("You're not in a voice channel!")

    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()


@bot.command()
async def leave(ctx):
    """Disconnects the bot from voice"""
    await ctx.voice_client.disconnect()


@bot.command()
async def clear(ctx):
    await ctx.send('clear')
    return


#@bot.command()
#async def help(ctx):
#    await ctx.send('help')
#    return


@bot.command()
async def skip(ctx):
    await ctx.send('skip')
    return


@bot.command()
async def play(ctx, *, arg):
    """Play the given song"""
    print(ctx.author)
    if 'youtube' in arg:
        await ctx.send('youtube')
    elif 'spotify' in arg:
        await ctx.send('spotify')
    else:
        await ctx.send(arg)
    return

with open('../token', encoding='utf-8') as f:
    token = f.read()

bot.run(token)
