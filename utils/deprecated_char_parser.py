from __future__ import annotations
import re
from typing import Dict, List
import json

with open('./utils/char_dict.json') as f:
    char_dict: Dict[str, List[str]] = json.load(f)
    print(
        'char_dict loaded with {rows} rows'.format(rows=len(char_dict.keys())))


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
