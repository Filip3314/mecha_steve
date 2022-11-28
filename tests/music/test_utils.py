import mecha_steve.music.utils as utils
import pytest
from requests.exceptions import HTTPError
    
@pytest.mark.asyncio
async def test_empty_arg():
    with pytest.raises(ValueError):
        await utils.find_audio_online("")
    with pytest.raises(ValueError):
        await utils.find_audio_online(None)
    with pytest.raises(ValueError):
        await utils.find_audio_online(False)

@pytest.mark.asyncio
async def test_youtube_url():
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("https://www.youtube.com/watch?v=dQw4w9WgXcQ")).title
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("www.youtube.com/watch?v=dQw4w9WgXcQ")).title
    assert "sniffer.avi" == (await utils.find_audio_online("https://www.youtube.com/watch?v=SCZI7fZJlgE")).title
    assert "sniffer.avi" == (await utils.find_audio_online("https://youtu.be/SCZI7fZJlgE")).title
    assert "sniffer.avi" == (await utils.find_audio_online("http://youtu.be/SCZI7fZJlgE")).title
    assert "googlevideo.com" in (await utils.find_audio_online("youtu.be/SCZI7fZJlgE")).url


@pytest.mark.asyncio
async def test_search():
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("youtube never gonna give you up")).title
    assert "sniffer.avi" == (await utils.find_audio_online("sniffer.avi")).title

@pytest.mark.asyncio
async def test_fake_well_formed_url():
    assert "googlevideo.com" in (await utils.find_audio_online("https://sadfjdslkj.com")).url

@pytest.mark.asyncio
async def test_malformed_url():
    assert "googlevideo.com" in (await utils.find_audio_online("htp://youtube.bruh")).url

@pytest.mark.asyncio
async def test_404():
    with pytest.raises(HTTPError):
        assert await utils.find_audio_online("youtube.com/bruh")
    with pytest.raises(HTTPError):
        assert await utils.find_audio_online("https://youtube.com/bruh")
    with pytest.raises(HTTPError):
        assert await utils.find_audio_online("https://google.com/wrong_address")
    with pytest.raises(HTTPError):
        assert await utils.find_audio_online("https://open.spotify.com/track/7sfljKs4VCY1wFebnOdJrM13t6?si=320c5c1d8a704266")
        
    
@pytest.mark.asyncio
async def test_spotify_url():
   assert "Gas Gas Gas" in (await utils.find_audio_online("https://open.spotify.com/album/0uhTliVFDT7CCzitqtW4KA")).title
