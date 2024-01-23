from datetime import date
import discord
from db import GameRecord
from util import ping_to_userid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union, List
    from bot import BotClient

def find_score2(frags: List[str]) -> Union[list[tuple[str, int]], None]:
    tot = 0
    score_list = []
    for i in range(3, 11, 2):
        tot += float(frags[i + 1])
    if 90 <= tot <= 100 and abs(round(tot) - tot) < 1e-6:
        for i in range(3, 11, 2):
            usr_id = ping_to_userid(frags[i])
            score = float(frags[i + 1])
            score_list.append((usr_id, 100 * round(10 * score)))
        return score_list
    elif tot % 1000 == 0:
        for i in range(3, 11, 2):
            usr_id = ping_to_userid(frags[i])
            score = int(frags[i + 1])
            score_list.append((usr_id, 100 * round(10 * score)))
        return score_list
    else:
        return None


async def on_cmd_db_store(self: BotClient, message: discord.Message, frags: List[str]):
    players = find_score2(frags)
    if players is None:
        raise RuntimeError("Invalid Data")
    record = GameRecord("discord:" + message.id, str(date.today()), [v[0] for v in players], [v[1] for v in players])
    self.db.new_game(record)
    await message.add_reaction('✅')


async def on_cmd_db_get(self: BotClient, message: discord.Message, frags: List[str]):
    # frags[3] is user id
    if len(frags) != 4:
        raise RuntimeError("Not enough/too many arguments!")
    usr = self.db.get_user_games(ping_to_userid(frags[3]))
    out = ''
    for e in usr:
        out = out + str(e) + "\n"
    await message.channel.send(out)