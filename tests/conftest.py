import pytest_asyncio
import discord.ext.test as dpytest
from mecha_steve import make_bot


@pytest_asyncio.fixture
async def bot():
    test_bot = await make_bot()
    await test_bot._async_setup_hook()
    dpytest.configure(test_bot)
    return test_bot


@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()
