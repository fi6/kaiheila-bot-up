from __future__ import annotations
import os
import re
from typing import Dict, List, Match
import logging
import json

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

with open('./core/__video/char_all.json') as f:
    char_dict: Dict[str, List[str]] = json.load(f)
    logging.debug(
        'char_dict loaded with {rows} rows'.format(rows=len(char_dict.keys())))

match_translation = {'winners': '胜者组', 'losers': '败者组'}


def char_parser(char_str: str) -> List[str]:
    characters = re.split(r'[,，]', char_str)
    result: List[str] = []
    for char in characters:
        code = __get_code(char)
        if code is not None:
            result.append(code)
    return result


def __get_code(char: str) -> str | None:
    for code, names in char_dict.items():
        if char == code:
            return code
        else:
            for name in names:
                if char.lower() == name.lower():
                    return code


def get_name_by_code(code: str) -> str | None:
    if code in char_dict.keys():
        return char_dict[code][0]


def get_name_by_codes(codes: List[str]) -> str:
    """
    throw error if key does not exist. should not happen!
    """
    result = []
    for code in codes:
        result.append(char_dict[code][0])
    return ', '.join(result)


def replace_name(match: Match):
    chars = match.group(1).split(',')
    result: List[str] = map(lambda x: parse_to_code(x), chars)
    return '({})'.format(', '.join(result))


def parse_to_code(char: str) -> str:
    for key, items in char_dict.items():
        for name in items:
            if (char.lower() == name.lower()):
                return key
            score = fuzz.token_sort_ratio(char.lower(), name.lower())
            if score > 83:
                # print(char, name)
                return key
    # for key, items in char_dict.items():
    #     for name in items:
    #         score = fuzz.partial_token_sort_ratio(char.lower(), name.lower())
    if re.search(r'(Pokémon|pokemon)', char, re.IGNORECASE):
        return '33'
    raise ValueError('code not found for char: ', char)


def char_crawler(path: str):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, 'ja.html')
    soup = BeautifulSoup(open(abs_file_path), "html.parser")
    # print(soup.prettify())
    for item in soup.find_all('li'):
        if not item.a:
            continue
        url = item.a['href']
        num = re.match(r'.+?([0-9]+\w?.*)\.html', url)[1].upper()
        name = item.find(attrs={'class': 'fighter-list__name-main'}).get_text()