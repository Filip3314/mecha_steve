import discord.ext.test as dpytest
import pytest

@pytest.mark.asyncio
async def test_bot_help(bot):
    await dpytest.message("$help")
    assert dpytest.verify().message().content("This is a very helpful message!")
    await dpytest.empty_queue()

@pytest.mark.asyncio
async def test_nothing():
    assert dpytest.verify().message().nothing()
