"""Functions to offload work to. Helps enable testing of the app"""
import discord
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
        'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


async def get_song(arg):
    """Figures out the song to play based on the argument passed in"""
    if 'youtube' in arg:
        data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(arg,
                                                                                              download=True))
        filename = ytdl.prepare_filename(data)
        return discord.FFmpegPCMAudio(filename, **ffmpeg_options)
    if 'spotify' in arg:
        return 'A spotify link!'
    return 'Gotta search for this!'
