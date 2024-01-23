from __future__ import annotations

import functools

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union

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


def ping_to_userid(s: str) -> str:
    return functools.reduce(lambda a, b: a + b, [i for i in s if i.isnumeric()])