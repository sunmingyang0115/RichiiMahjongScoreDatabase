from __future__ import annotations

from datetime import date
import datetime
import time
import discord
from db import GameRecordNya
from embed_helper import send_command_embed
from mjgame import MJGameNya
from util import ping_to_userid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from bot import BotClient

import io

async def on_cmd_db_csv(self: BotClient, message: discord.Message, frags: list[str]):
    usrg = io.StringIO()
    usrs = io.StringIO()
    self.db.export_as_csv(usrg, usrs)

    file1 = discord.File(fp=io.BytesIO(usrg.getvalue().encode()), filename='games.csv')
    file2 = discord.File(fp=io.BytesIO(usrs.getvalue().encode()), filename='scores.csv')

    await message.channel.send(files=[file1,file2])

async def on_cmd_db_lb_stats(self: BotClient, message: discord.Message, frags: list[str]):
    await send_command_embed(self, message.channel, self.db.list_user_stats(frags[3], 10), "Leaderboard", message.author)


async def on_cmd_db_new_game(self: BotClient, message: discord.Message, frags: list[str]):
    unix = int(time.time())
    nfrags = frags[3:]
    mjgame = MJGameNya(unix, str(message.id), MJGameNya.parse_input(nfrags))
    self.db.new_game(GameRecordNya.from_mjgame(mjgame))

async def on_cmd_db_usr(self: BotClient, message: discord.Message, frags: list[str]):
    await send_command_embed(self, message.channel, self.db.get_user_games(frags[3]), "User Statistics", message.author)

async def on_cmd_db_del(self: BotClient, message: discord.Message, frags: list[str]):
    self.db.delete_game(frags[3])

async def on_cmd_db_get_game(self: BotClient, message: discord.Message, frags: list[str]):
    gmrcd = self.db.get_game(frags[3])
    await send_command_embed(self, message.channel, [gmrcd.game_id, gmrcd.date, gmrcd.users, gmrcd.final_scores], "Game Statistics", message.author)


# async def on_cmd_db_store(self: BotClient, message: discord.Message, frags: list[str]):
#     # ron db store


# async def on_cmd_db_get(self: BotClient, message: discord.Message, frags: list[str]):
#     # frags[3] is user id
#     if len(frags) != 4:
#         raise RuntimeError("Not enough/too many arguments!")
#     usr = self.db.get_user_games(ping_to_userid(frags[3]))
#     out = ''
#     for e in usr:
#         out = out + str(e) + "\n"
#     await message.channel.send(out)
