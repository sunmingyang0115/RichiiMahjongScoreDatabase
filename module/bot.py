from typing import Any

import discord
from discord import Intents

from cmds.cmd_db import on_cmd_db_store, on_cmd_db_get
from cmds.cmd_ping import on_cmd_ping
from db import Database


class BotClient(discord.Client):
    prefix = "ron"

    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.db = Database()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        frags = message.content.split()
        print(frags)
        if message.author == self.user or frags[0] != BotClient.prefix:
            return
        try:
            if frags[1] == 'ping':
                await on_cmd_ping(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'store':
                await on_cmd_db_store(self, message, frags)
            elif frags[1] == 'db' and frags[2] == 'get':
                await on_cmd_db_get(self, message, frags)
            elif message.channel.id == 1175888656532262942:
                await on_cmd_db_store(self, message, ["ron", "db", "store"] + frags)
        except Exception as err:
            await message.channel.send("An error has occured: ```" + str(err.args[0]) + "```")
