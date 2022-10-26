"""Music related commands for Mecha Steve"""
from discord.ext import commands


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
    return await ctx.send(get_song(arg))


def get_song(arg):
    """Figures out the song to play based on the argument passed in"""
    if 'youtube' in arg:
        return 'A youtube link!'
    if 'spotify' in arg:
        return 'A spotify link!'
    return 'Gotta search for this!'


@commands.command()
async def join(ctx):
    """Joins the voice channel the user who send the command is in"""
    user_channel = get_user_channel(ctx)
    if user_channel is None:
        return await ctx.send("You're not in a voice user_channel!")

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(user_channel)
    else:
        await user_channel.connect()


def get_user_channel(ctx):
    """Returns the channel that the Author in th given context is in"""
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        channel = None
    return channel


@commands.command()
async def leave(ctx):
    """Disconnects the bot from voice"""
    await ctx.voice_client.disconnect()
