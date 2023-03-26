import pytest_asyncio
import discord.ext.test as dpytest
from mecha_steve import make_bot
import glob
import os


@pytest_asyncio.fixture
async def bot():
    test_bot = await make_bot(None)
    await test_bot._async_setup_hook()
    dpytest.configure(test_bot)
    return test_bot


@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()

def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob('./dpytest_*.dat')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)