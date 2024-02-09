# from __future__ import annotations

# from datetime import date
# import discord
# from db import GameRecordNya
# from util import ping_to_userid

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from typing import Union
#     from bot import BotClient



# # async def on_cmd_db_store(self: BotClient, message: discord.Message, frags: list[str]):
# #     # ron db store


# async def on_cmd_db_get(self: BotClient, message: discord.Message, frags: list[str]):
#     # frags[3] is user id
#     if len(frags) != 4:
#         raise RuntimeError("Not enough/too many arguments!")
#     usr = self.db.get_user_games(ping_to_userid(frags[3]))
#     out = ''
#     for e in usr:
#         out = out + str(e) + "\n"
#     await message.channel.send(out)
