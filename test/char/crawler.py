import csv
import json
import os

os.path.join('.')
import re
from urllib import request

from bs4 import BeautifulSoup

# source = request.urlopen(
#     'https://www.smashbros.com/ja_JP/fighter/index.html').read()
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in


def parse(file_name: str = 'cn.html'):
    abs_file_path = os.path.join(script_dir, file_name)
    soup = BeautifulSoup(open(abs_file_path), "html.parser")
    # print(soup.prettify())
    char_dict = {}
    for item in soup.find_all('li'):
        if not item.a:
            continue
        url = item.a['href']
        num = re.match(r'.+?([0-9]+\w?.*)\.html', url)[1].upper()
        name = item.find(attrs={'class': 'fighter-list__name-main'}).get_text()
        char_dict[num] = name


def get_from_csv():
    path = os.path.join(script_dir, 'char_all.csv')
    char_dict = {}
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            char_dict[row[0]] = [item for item in row[1:] if item != '']
            char_dict[row[0]]
    with open(os.path.join(script_dir, 'char_all.json'), 'w') as f:
        f.write(json.dumps(char_dict))


get_from_csv()