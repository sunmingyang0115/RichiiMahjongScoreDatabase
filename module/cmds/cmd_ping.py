from __future__ import annotations

import discord

from typing import TYPE_CHECKING

from embed_helper import send_command_embed
if TYPE_CHECKING:
    from bot import BotClient

async def on_cmd_ping(self: BotClient, message: discord.Message, frags: list[str]):
    await send_command_embed(
                            self,
                            message.channel,
                            [':ping_pong: {0}'.format(round(self.latency, 2))],
                            "Ping",
                            message.author)