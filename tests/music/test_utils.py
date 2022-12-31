import mecha_steve.music.utils as utils
import pytest
from youtube_dl import DownloadError
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
async def test_quoted_url():
    assert "googlevideo.com" in (await utils.find_audio_online("\"/google.com/bruh_moment\"")).url
    assert "googlevideo.com" in (await utils.find_audio_online("\"https://google.com/bruh_moment\"")).url
    assert "googlevideo.com" in (await utils.find_audio_online("\"ytsearch:google.com/bruh_moment\"")).url
    assert "googlevideo.com" in (await utils.find_audio_online("ytsearch:\"https://google.com/bruh_moment\"")).url
    assert "googlevideo.com" in (await utils.find_audio_online("ytsearch:\"ytsearch:google.com/bruh_moment\"")).url

@pytest.mark.asyncio
async def test_search():
    assert "Never Gonna Give You Up" in (await utils.find_audio_online("youtube never gonna give you up")).title
    assert "sniffer.avi" == (await utils.find_audio_online("sniffer.avi")).title

@pytest.mark.asyncio
async def test_fake_http_url():
    with pytest.raises(DownloadError):
        await utils.find_audio_online("https://sadfjdslkj.com")

@pytest.mark.asyncio
async def test_404():
    with pytest.raises(DownloadError):
        assert await utils.find_audio_online("youtube.com/bruh")
    
@pytest.mark.asyncio
async def test_no_source_url():
    with pytest.raises(DownloadError):
        assert await utils.find_audio_online("https://bing.com")

@pytest.mark.asyncio
async def test_spotify_url():
    with pytest.raises(DownloadError):
        assert "Gas Gas Gas" in (await utils.find_audio_online("https://open.spotify.com/album/0uhTliVFDT7CCzitqtW4KA")).title
    with pytest.raises(DownloadError):
        assert "Graceland Too" in (await utils.find_audio_online("https://open.spotify.com/track/1WCjhRs2WBgyeGaybCX2Po?si=1e2ea4843bc441c6")).title

@pytest.mark.asyncio
async def test_bandcamp_url():
    assert "Diamond's Shining Face" in (await utils.find_audio_online("https://godcaster.bandcamp.com/track/diamonds-shining-face")).title
