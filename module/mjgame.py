from typing import TYPE_CHECKING
import copy
if TYPE_CHECKING:
    from typing import Union
import re


class MJGameNya():
    def get_date(self) -> int:
        return self._date
    
    def get_gameid(self) -> str:
        return self._gameid
    
    def get_raw_scores(self) -> dict[str, int]:
        return self._raw_scores

    def __init__(self, date:int, gameid:str, raw_scores:dict[str, int]):
        self._date = date
        self._gameid = gameid
        self._raw_scores = raw_scores   
    
    def get_users_ordered(self):
        lst = list(self._raw_scores.items())
        lst.sort(key=lambda x: -x[1])
        return list(map(lambda x: x[0], lst))


    def get_winner(self) -> str:
        return self.get_users_ordered()[0]

    def convert_to_adjusted(score_dict:dict[str,int]) -> dict[str,int]:
        uma = [15000, 5000, -5000, -15000]
        adj_dict = {}
        for i, k in enumerate(score_dict.keys()):
            adj_dict[k] = uma[i] + score_dict[k]
        return adj_dict
    
    def parse_input(bar: list[str]) -> dict[int, int|float] | None:
        if len(bar) != 8 or not all(isinstance(s, str) for s in bar):
            return None
        
        re_uid = r"<@\d*>"
        if (not all(re.match(re_uid, s) and
                    re.match(re_uid, s)[0] == s for s in bar[::2])
            or not all(s.replace('.', '', 1).isdigit() for s in bar[1::2])):
            return None
        
        if len(set(bar[::2])) < 4:
            return None

        uid = [s[2:-1] for s in bar[::2]]
        scores = [float(s) for s in bar[1::2]]
        
        if sum(scores) >= 100000:
            return None
        if sum(scores) <= 100:
            scores = [int(1000*s) for s in scores]
        
        return (dict(zip(uid, scores)))
