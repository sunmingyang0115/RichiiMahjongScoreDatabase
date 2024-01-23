import discord

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from bot import BotClient

async def on_cmd_ping(self: BotClient, message: discord.Message, frags: List[str]):
    await message.channel.send('pong')