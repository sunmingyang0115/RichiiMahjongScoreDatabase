from __future__ import annotations

import discord

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import BotClient

async def on_cmd_ping(self: BotClient, message: discord.Message, frags: list[str]):
    await message.channel.send('pong')