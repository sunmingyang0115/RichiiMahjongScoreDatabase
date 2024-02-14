from __future__ import annotations

import discord

# from cmds.cmd_db import on_cmd_db_store, on_cmd_db_get
from cmds.cmd_ping import on_cmd_ping
from db import DatabaseNya
from embed_helper import send_command_embed, send_simple_embed

from typing import TYPE_CHECKING

from cmds.cmd_db import on_cmd_db_csv, on_cmd_db_del, on_cmd_db_get_game, on_cmd_db_lb_stats, on_cmd_db_new_game, on_cmd_db_usr
if TYPE_CHECKING:
    from typing import Any
    from discord import Intents


class BotClient(discord.Client):
    prefix = "ron"

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.db = DatabaseNya()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        frags = message.content.split()
        print(frags)
        if message.author == self.user or len(frags) == 0 or frags[0] != BotClient.prefix:
            return
        try:
            if frags[1] == 'ping':
                await on_cmd_ping(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'csv':
                await on_cmd_db_csv(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'lb':
                await on_cmd_db_lb_stats(self, message, frags)
                # "games_played"
                # "games_won"
                # "avg_rank"
            elif frags[1] == 'db' and frags[2] == 'newgame':
                await on_cmd_db_new_game(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'usr':
                await on_cmd_db_usr(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'del' and message.author.id == 372123318167273502:
                await on_cmd_db_del(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'getgame':
                await on_cmd_db_get_game(self, message, frags)
        except Exception as err:
            await send_simple_embed(self,
                                     message.channel,
                                     "An error has occured",
                                     [":(", str(err)])
            raise