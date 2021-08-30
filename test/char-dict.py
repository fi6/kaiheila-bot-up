import sys

sys.path.append('.')
import csv
import json
import re

file = 'test/char.csv'
char_dict = {}
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            char_dict[row[0]] = [
                row[1], row[2], row[3], *re.split(r'[/，]', row[4])
            ] if row[4] else [row[1], row[2], row[3]]
            line_count += 1
            print(row[0], char_dict[row[0]])
    print(f'Processed {line_count} lines.')

with open('./utils/char_dict.json', 'w') as f:
    f.write(json.dumps(char_dict))
