"""Functions to offload work to. Helps enable testing of the app"""
import discord
import youtube_dl
import asyncio
import requests
import json

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
   'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False, 'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
        'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class MechaSource(discord.PCMVolumeTransformer):
    def __init__(self, source, url, title):
        self.original = source
        self. url = url
        self.title = title

async def find_audio_online(arg):
    """Returns an audio stream that best matches the given argument."""
    if arg == "":
        return None
    url = arg if arg.startswith('http') else 'https://' + arg
    response = requests.get(url)
    data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(arg,
                                                                                      download=False))
    if response.status_code < 400:
        source = data
    else:
        source = data['entries'][0]

    audio_url = source['url']
    title = source['title']

    return MechaSource(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), audio_url, title)
