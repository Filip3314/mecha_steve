import mecha_steve.music.utils as utils
import pytest
    
@pytest.mark.asyncio
async def test_find_audio_online_empty_arg():
    assert await utils.find_audio_online("") == None

@pytest.mark.asyncio
async def test_find_audio_online_valid_youtube_url():
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("https://www.youtube.com/watch?v=dQw4w9WgXcQ")).title
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("www.youtube.com/watch?v=dQw4w9WgXcQ")).title
    assert "sniffer.avi" == (await utils.find_audio_online("https://www.youtube.com/watch?v=SCZI7fZJlgE")).title
    assert "sniffer.avi" == (await utils.find_audio_online("https://youtu.be/SCZI7fZJlgE")).title
    assert "sniffer.avi" == (await utils.find_audio_online("http://youtu.be/SCZI7fZJlgE")).title
    assert "sniffer.avi" == (await utils.find_audio_online("youtu.be/SCZI7fZJlgE")).title


@pytest.mark.asyncio
async def test_find_audio_online_search():
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("youtube never gonna give you up")).title
    assert "sniffer.avi" == (await utils.find_audio_online("sniffer.avi")).title

@pytest.mark.asyncio
async def test_find_audio_online_invalid_url():
    return
    
@pytest.mark.asyncio
async def test_find_audio_online_spotify_url():
   assert "Gas Gas Gas" in (await utils.find_audio_online("https://open.spotify.com/album/0uhTliVFDT7CCzitqtW4KA")).title
