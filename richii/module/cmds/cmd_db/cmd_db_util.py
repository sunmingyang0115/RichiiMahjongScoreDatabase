import functools
from datetime import date
from typing import Union, List, Callable
from richii.module.db import Database, GameRecord


def parse_ping(s: str) -> Union[int, None]:
    if (not s.startswith("<@")) or (not s.endswith(">")):
        return None
    s = s[2:-1]
    if s.startswith("!"):
        s = s[1:]
    try:
        return int(s)
    except:
        return None


def car(lst):
    return lst[0]


def cdr(lst):
    return lst[1:]


def test(a: int):
    a.bit_count()


# async def isValid(frags: List[str]):
#     numbers = [1, 3, 5, 7]
#     texts = [0, 2, 4, 6]
#
#     ping_to_userid = lambda x : functools.reduce(lambda a, b : a+b, [i for i in x if i.isnumeric()])
#

async def command_fetch(frags: List[str], db: Database):
    if len(frags) != 4:
        raise RuntimeError("Not enough/too many arguments!")
    return db.get_user_games(frags[3])


async def command_store(frags: List[str], msg_id: str, db: Database):
    if len(frags) != 11:
        raise RuntimeError("Not enough/too many arguments!")
    players = []
    for i in range(3, 11, 2):
        ping = parse_ping(frags[i])
        if ping is None:
            raise RuntimeError(f"{i + 1}th argument is not a ping")
        money = None
        try:
            money = int(frags[i + 1])
        except:
            raise RuntimeError(f"{i + 2}th argument isn't an integer")
        players.append((ping, money))
    record = GameRecord("discord:"+msg_id, str(date.today()), [v[0] for v in players], [v[1] for v in players])
    db.new_game(record)


# returns dictionary
def findscore(inputstring):
    # replace with input() later
    entries = inputstring.split("\n")
    scoredict = {}
    tot = 0
    for entry in entries:
        scorepair = entry[2:].split(">")
        tot += float(scorepair[1])
    if 90 <= tot <= 100 and abs(round(tot) - tot) < 1e-6:
        for entry in entries:
            scorepair = entry[2:].split(">")
            scoredict[int(scorepair[0])] = 100 * round(10 * float(scorepair[1]))
        '''
    ret = ""
    for player in scoredict:
        ret += "<@" + str(player) + ">" + " " + str(scoredict[player]) + "\n"
    '''
        return scoredict;
    elif tot % 1000 == 0:
        for entry in entries:
            scorepair = entry[2:].split(">")
            scoredict[int(scorepair[0])] = int(scorepair[1])
        '''
    ret = ""
    for player in scoredict:
        ret += str(player) + " " + str(scoredict[player]) + "\n"
    '''
        return scoredict;
    else:
        return "troll nya~"


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message[0] == '<':
        print(findscore(p_message))  # outputs the dictionary in console
        return 'scores saved'

    if p_message == '!help':
        return '`this is a help message nya~`'

    return 'I didn\'t understand what u said nya~~'

