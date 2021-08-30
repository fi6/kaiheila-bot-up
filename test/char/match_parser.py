import sys
sys.path.append('.')

import os
import re
from typing import Callable, List, Match

import json
from fuzzywuzzy import fuzz

matches = """
Free Agent BestNess (Ness) vs Bandits Sonix (Sonic) Grand Final
8BitMan (R.O.B.) vs Bandits Sonix (Sonic) Losers Semis
Bandits Sonix (Sonic) vs Sharp (Pyra Mythra, Wolf) Losers Quarters
SassyFlygon (Luigi) vs BestNess (Ness, Piranha Plant) Winners Finals
SassyFlygon (Luigi) vs Bandits Sonix (Sonic) Losers Finals
SassyFlygon (Luigi) vs 8BitMan (R.O.B.) Winners Semis
Bandits Sonix (Sonic) vs Free Agent BestNess (Ness) Winners Semis
Grayclash (Bayonetta) vs 8BitMan (Diddy Kong) Losers Quarter
Kagaribi 4 Losers Semis - Zackray (Joker) Vs. Hero (Bowser) SSBU Smash Ultimate
CEO 2019 SSBU - FOX | MkLeo (Joker) Vs. PG | Marss (ZSS, Falcon) Smash Ultimate Grand Finals
Frostbite 2020 SSBU Losers Top 32 - MkLeo (Joker) Vs MVG | Salem (Hero, Dark Samus) Ultimate Singles
zackray vs MastaMario - Pools Winners' Semifinals: Ultimate Singles - TBH9 | Joker vs Mario
MSM Online 22 - Ashton (Young Link) Vs. NEST | Sharp (Joker) Grand Finals - Smash Ultimate
【#スマブラSP/#マエスマ】＜準決勝＞ひがちゃんまる(ガノンドロフ）VS そめ(ゲッコウガ)【1on1#226 オンライン大会/SSBU Online Tournament】
SNS5 SSBU - CLG | VoiD (Pichu) Vs. MVG | Dark Wizzy (Mario) Smash Ultimate Winner's Top 64
Genesis 6 - TSM | Leffen (Pokemon Trainer) vs dB | yeti (Mega Man) Top 32 - Smash Ultimate
"""

with open('./core/__video/char_all.json') as f:
    char_dict = json.load(f)


def replace_name(match: Match):
    chars = match.group(1).split(',')
    result: List[str] = map(lambda x: get_name(x), chars)
    return '({})'.format(', '.join(result))


def get_name(char: str):
    for key, items in char_dict.items():
        for name in items:
            if (char.lower() == name.lower()):
                return char_dict[key][0]
            score = fuzz.token_sort_ratio(char.lower(), name.lower())
            if score > 83:
                # print(char, name)
                return char_dict[key][0]
    for key, items in char_dict.items():
        for name in items:
            score = fuzz.partial_token_sort_ratio(char.lower(), name.lower())
            if score > 83:
                return char_dict[key][0]
    return char


def translate_group(string):
    def replace_with_result(string: str, regex: str, replace: Callable):
        result = []
        string_after = re.sub(
            regex, lambda x: result.append(x.group(0)) or replace(x), string,
            0, re.IGNORECASE)
        return string_after, result

    def grand(string: str):
        return replace_with_result(string,
                                   r'(grand ?fin.+?)(?:\'?s?\'?)(?:\b|$)',
                                   lambda x: '总决赛')

    def win_lose(string: str):
        return replace_with_result(
            string, r'(winner|loser)(?:\'?s?\'?)', lambda x: '胜者组'
            if x.group(0).lower().startswith('w') else '败者组')

    def round(string: str):
        replacements = [('semi', '半决赛'), ('final', '决赛'), ('qua', '¼决赛'),
                        ('pool', '初赛'), ('bracket', '初赛')]
        _ = []
        for keyword, replace in replacements:
            string, _ = replace_with_result(
                string, f'({keyword}.+?)' + r'(?:\'?s?\'?)(?:\b|$)',
                lambda x: replace)
            # if len(_):
            #     print(_)
        return string, _

    string_after, result = grand(string)
    if len(result):
        return string_after

    string_after, result = win_lose(string_after)

    string_after, _ = round(string_after)

    return string_after


# for row in matches.splitlines():
#     chared = re.sub(r'(?:\(|\（)(.+?)(?:\)|\）)', replace_name, row)
#     print(translate_group(chared))


def main():
    # get_name('ガノンドロフ')
    for row in matches.splitlines():
        chared = re.sub(r'(?:\(|\（)(.+?)(?:\)|\）)', replace_name, row)
        print(translate_group(chared))
    # get_name()


main()