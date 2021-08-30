import re
import logging
from typing import List, Match, Sequence
from dataclasses import dataclass

from .__char import parse_to_code, get_name_by_code, get_name_by_codes

player_fighter_regex = r'(?P<p1>(?:\b\w+ ?\|? ?)*?(?:\w|\[|\])+ *)(?:[(（](?P<f1>.+?)[)）])(?: *vs\.? *)(?P<p2>(?:\b\w+ ?\|? ?)*?(?:\w|\[|\])+ *)(?:[(（](?P<f2>.+?)[)）])'  # noqa


class MatchInfo():
    title: str
    match_name: str = ''
    p1: str = ''
    p1_fighter: List[str] = []  # p1 fighter in code
    p2: str = ''
    p2_fighter: List[str] = []
    pool: bool = False
    grand_final: bool = False
    winner: bool = False
    loser: bool = False
    round: str = ''
    corrected: bool = False

    def __init__(self, title: str) -> None:
        self.title = title

    @property
    def format_title(self):
        return ' '.join(
            filter(lambda x: x is not None, [
                self.match_name, self._format_round, self.p1,
                self.get_fighter_str(self.p1_fighter), 'Vs.', self.p2,
                self.get_fighter_str(self.p2_fighter), '任天堂明星大乱斗'
            ]))

    @staticmethod
    def get_fighter_str(fighter_list: List[str]):
        return ('(' + get_name_by_codes(fighter_list) + ')')

    @property
    def _format_round(self):
        if self.grand_final:
            return '总决赛'
        main = None
        if self.winner:
            main = '胜者组'
        elif self.loser:
            main = '败者组'
        pre = '初赛' if self.pool else None
        tail = self.round if len(self.round) else None
        elements = [pre, main, tail]
        if not any(elements):
            return None
        return ' '.join(filter(lambda x: x is not None, elements))

    def to_string(self):
        return '比赛名: {match}\n轮次: {round}\n选手1: {p1_name} 角色: {p1_char}\n选手2: {p2_name} 角色: {p2_char}'.format(
            match=self.match_name,
            round=self._format_round,
            p1_name=self.p1,
            p1_char=self.get_fighter_str(self.p1_fighter),
            p2_name=self.p2,
            p2_char=self.get_fighter_str(self.p2_fighter))

    def from_string(self, text: str):
        lines = text.splitlines()
        if len(lines) != 4:
            raise ValueError('格式不正确，请确认文字是否为4行')
        result = re.match(r'^(?:比赛名: )(.+)$', lines[0])
        if not result:
            raise ValueError('格式不正确，请确认第1行开头是否为 比赛名: ')
        self.match_name = result.group(1)
        result = re.match(r'^(?:轮次: )(.+)$', lines[1])
        if not result:
            raise ValueError('格式不正确，请确认第2行开头是否为 轮次: ')
        self.round = result.group(1)
        result = re.match(r'^(?:选手1: )(.+?)(?: 角色: )(.+)$', lines[2])
        if not result:
            raise ValueError('格式不正确，请确认第3行开头是否为 选手1: ')
        self.p1 = result.group(1)
        self.p1_fighter = _get_codes(result.group(2))
        result = re.match(r'^(?:选手2: )(.+)(?: 角色: )(.+)$', lines[3])
        if not result:
            raise ValueError('格式不正确，请确认第4行开头是否为 选手2: ')
        self.p2 = result.group(1)
        self.p2_fighter = _get_codes(result.group(2))


def parse(title: str):
    if not len(title):
        return None
    match_info = MatchInfo(title=title)
    try:
        title, match_info = get_player_fighter(title, match_info)
        title, match_info = get_round(title, match_info)
        return match_info
    except Exception as e:
        logging.exception(e)
        return match_info


def _get_codes(char_string: str):
    chars = re.split(r'[,，/]', char_string)
    return list(map(lambda x: parse_to_code(x), chars))


def __replace_name(match: Match):
    p1_fighter = _get_codes(match.group(2))
    p2_fighter = _get_codes(match.group(4))
    return '{} ({}) Vs. {} ({})'.format(
        match.group(1).strip(), get_name_by_codes(p1_fighter),
        match.group(3).strip(), get_name_by_codes(p2_fighter))


def get_player_fighter(title, match_info: MatchInfo):
    def replace_and_append(match: Match, result: List):
        result.append(match)
        return __replace_name(match)

    result = []
    title = re.sub(player_fighter_regex,
                   lambda x: replace_and_append(x, result), title, 0,
                   re.IGNORECASE)
    if not len(result):
        logging.warning('cannot find player/fighter, no result: ', title)
        raise ValueError()
    result = result[0]
    if not len(result.groups()) == 4:
        logging.warning('cannot find player/fighter, groups != 5: ', title,
                        result)
        raise ValueError()
    match_info.p1 = result.group(1).strip()
    match_info.p1_fighter = _get_codes(result.group(2))
    match_info.p2 = result.group(3).strip()
    match_info.p2_fighter = _get_codes(result.group(4))
    return title, match_info


def get_round(title: str, match_info: MatchInfo):
    def replace_with_result(string: str, match: str, replace: str):
        result = []
        match = match + r'(?:\'?s?\'?)(?:\b|$)'
        return re.sub(match, lambda x: result.append(replace) or replace,
                      string, 0,
                      re.IGNORECASE), result[0] if len(result) else None

    # look for game name
    result = re.search(r'(^.+?)(?: )*(?:top|ssbu|-|grand|win|los|pool|vs|＜)',
                       title, re.IGNORECASE)
    if result:
        match_info.match_name = result.group(1)

    # check grand
    title, result = replace_with_result(title, r'(grand ?fin.+?)', '总决赛')
    if result:
        match_info.grand_final = True
        return title, match_info

    # check if winner
    title, result = replace_with_result(title, r'(winner)', '胜者组')
    if result:
        match_info.winner = True
    else:
        # not winner, check if loser
        title, result = replace_with_result(title, r'(loser)', '败者组')
        if result:
            match_info.loser = True

    # check if pool
    title, result = replace_with_result(title, r'(pool|bracket)', '初赛')
    if result:
        match_info.pool = True

    # look for round step 1
    result = re.search(r'((?:round|top) \d+\b)', title, re.IGNORECASE)
    if result:
        match_info.round = result.group(1)
    # look for round step 2
    for keyword, replace in [(r'(semi)', '半决赛'), (r'(final)', '决赛'),
                             (r'(qua.+?)', '¼决赛'), (r'(eighth)', 'Top 8')]:
        title, result = replace_with_result(title, keyword, replace)
        if result:
            match_info.round = result
            break
    # look for round step 3
    result = re.search(r'\W(＜.+?＞)', title)
    if result:
        match_info.round = result.group(1)

    return title, match_info
