"""Music related commands for Mecha Steve"""

from discord.ext import commands
import utils
import discord
import youtube_dl
import asyncio
import queue

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn",
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class MechaSource(discord.PCMVolumeTransformer):
    """Wrapper for audio sources. Contains information necessary to communicate source being used to user."""

    def __init__(self, source, url, title):
        self.original = source
        self.url = url
        self.title = title
        self._volume = 1


async def find_audio_online(arg):
    """Returns an audio stream that best matches the given argument."""
    if not arg:
        raise ValueError("find_audio_online needs a non-empty input to search")
    if arg.startswith('"') and arg.endswith('"'):
        arg = "ytsearch:" + arg

    data = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ytdl.extract_info(arg, download=False)
    )

    if "entries" in data.keys():  # checking if data is a search result or not
        source = data["entries"][0]
    else:
        source = data

    audio_url = source["url"]
    title = source["title"]

    return MechaSource(
        discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), audio_url, title
    )


class Music(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger
        self.queue = queue.Queue()

    @commands.command()
    @utils.enforce_in_same_voice_channel()
    async def clear(self, ctx):
        """Removes all the songs in the queue and stops playing music"""
        await ctx.send("clear")
        return

    @commands.command()
    @utils.enforce_in_same_voice_channel()
    async def skip(self, ctx):
        """Skips the current song and plays the next one (if it exsits)"""
        await ctx.send("skip")
        return

    @commands.command(aliases=['p'])
    @utils.enforce_in_same_voice_channel()
    async def play(self, ctx, *, arg=""):
        """Plays the given song"""
        self.logger.info("Trying to play: " + arg)
        try:
            source = await find_audio_online(arg)
        except ValueError:
            return await ctx.send(
                "Play needs a search or URL input to play a song. See $help for more info."
            )
        except youtube_dl.DownloadError as err:
            return await ctx.send(str(err))
        ctx.voice_client.play(source)
        await ctx.send("Now playing " + source.title)
        return 0

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
    @utils.enforce_in_same_voice_channel()
    async def leave(self, ctx):
        """Disconnects the bot from voice"""
        await ctx.voice_client.disconnect()
