from typing import List
import discord

from bot import BotClient

async def on_cmd_ping(self: BotClient, message: discord.Message, frags: List[str]):
    await message.channel.send('pong')