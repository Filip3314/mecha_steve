"""Music related commands for Mecha Steve"""
from discord.ext import commands
import music.music_utils as utils


async def setup(bot: commands.Bot):
    """Adds all the commands in this module to the given bot"""
    bot.add_command(skip)
    bot.add_command(play)
    bot.add_command(clear)
    bot.add_command(join)
    bot.add_command(leave)


@commands.command()
async def clear(ctx):
    """Removes all the songs in the queue and stops playing music"""
    await ctx.send('clear')
    return


#@commands.command()
#async def help(ctx):
#    await ctx.send('help')
#    return


@commands.command()
async def skip(ctx):
    """Skips the current song and plays the next one (if it exsits)"""
    await ctx.send('skip')
    return


@commands.command()
async def play(ctx, *, arg):
    """Plays the given song"""
    source = utils.get_source(arg)
    await ctx.voice_client.play(source)
    return await ctx.send("Now playing" + source.title)


@commands.command()
async def join(ctx):
    """Joins the voice channel the user who send the command is in"""
    if ctx.author.voice is None:
        return await ctx.send("You're not in a voice user_channel!")

    user_channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(user_channel)
    else:
        await user_channel.connect()


@commands.command()
async def leave(ctx):
    """Disconnects the bot from voice"""
    await ctx.voice_client.disconnect()
