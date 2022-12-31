"""Music related commands for Mecha Steve"""
from discord.ext import commands
import youtube_dl
import music.utils as utils

class Music(commands.Cog):

    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger


    @commands.command()
    async def clear(self, ctx):
        """Removes all the songs in the queue and stops playing music"""
        await ctx.send('clear')
        return


    @commands.command()
    async def skip(self, ctx):
        """Skips the current song and plays the next one (if it exsits)"""
        await ctx.send('skip')
        return


    @commands.command(rest_is_raw=False)
    async def play(self, ctx, *, arg=""):
        """Plays the given song"""
        self.logger.info("Trying to play: " + arg)
        try:
            source = await utils.find_audio_online(arg)
        except ValueError:
            return await ctx.send("Play needs a search or URL input to play a song. See $help for more info.")
        except youtube_dl.DownloadError as err:
            return await ctx.send(str(err))
        ctx.voice_client.play(source)
        return await ctx.send("Now playing " + source.title)


    @commands.command()
    async def join(self, ctx):
        """Joins the voice channel the user who send the command is in"""
        if ctx.author.voice is None:
            return await ctx.send("You're not in a voice channel!")

        user_channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(user_channel)
        else:
            await user_channel.connect()


    @commands.command()
    async def leave(self, ctx):
        """Disconnects the bot from voice"""
        await ctx.voice_client.disconnect()
