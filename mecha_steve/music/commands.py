"""Music related commands for Mecha Steve"""

from discord.ext import commands

import utils
import discord
import yt_dlp
import asyncio

ytdlp_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "logtostderr": False,
    "quiet": False,
    "no_warnings": False,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(ytdlp_options)


class MechaSource(discord.PCMVolumeTransformer):
    """Wrapper for audio sources. Contains information necessary to communicate source being used to user."""

    def __init__(self, source, url, title):
        super().__init__(source)
        self.source = source
        self.url = url
        self.title = title
        self._volume = 1


async def find_audio_online(query):
    """Returns an audio stream that best matches the given argument."""
    if not query:
        raise ValueError("find_audio_online needs a non-empty input to search")
    if query.startswith('"') and query.endswith('"'):
        query = "ytsearch:" + query

    data = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ytdl.extract_info(query, download=False)
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
        self.queue = []

    @commands.command()
    @utils.enforce_in_same_voice_channel()
    async def clear(self, ctx):
        """Removes all the songs in the queue and stops playing music"""
        await ctx.send("clear")
        return

    @commands.command()
    @utils.enforce_in_same_voice_channel()
    async def skip(self, ctx):
        """Skips the current song and plays the next one (if it exists)"""
        voice = ctx.voice_client
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Skipping the current audio...')
        else:
            await ctx.send('Nothing to skip.')


    @commands.command(aliases=['p'])
    @utils.enforce_in_same_voice_channel()
    async def play(self, ctx, *, arg=""):
        ## playing songs
        # get input
        # find a source online/locally
        # add song to queue
        # determine whether to play the song immediately
        """Plays the given song"""
        self.logger.info("Trying to play: " + arg)
        voice = ctx.voice_client
        try:
            source = await find_audio_online(arg)
        except ValueError:
            return await ctx.send(
                "Play needs a search or URL input to play a song. See $help for more info."
            )
        except yt_dlp.DownloadError as err:
            return await ctx.send(str(err))
        self.queue.append(source)
        if not voice.is_playing():
            self.play_next(ctx)
        else:
            await ctx.send("Queued " + source.title)
        return 0

    def play_next(self, ctx):
        if len(self.queue) > 0:
            voice = ctx.voice_client
            source = self.queue.pop(0)
            try:
                voice.play(source, after=lambda x: self.play_next(ctx))
                #TODO fix this maybe? Not sure this is a good solution
                asyncio.run_coroutine_threadsafe(ctx.send(f'Now playing: {source.title}'), self.bot.loop)
            except:
                #TODO add exception handling
                pass

    @commands.command()
    async def song(self, ctx):
        #TODO add tests
        source = ctx.voice_client.source
        await ctx.send("[{0}]({1})".format(source.title, source.url))


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
