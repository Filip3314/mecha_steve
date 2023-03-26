from discord.ext.commands import (
    Command,
    Cog,
    HelpCommand
)
from typing import (
    Optional,
    List,
    Any,
    Mapping
)
import utils


class MechaSteveHelp(HelpCommand):
    """Custom implementation of the help command"""
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command[Any, ..., Any]]], /) -> None:
        await self.get_destination().send("This is a very helpful message!")
