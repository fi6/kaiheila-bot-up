from datetime import datetime
from ChineseTimeNLP import TimeNormalizer
# tn = TimeNormalizer(isPreferFuture=False)
from dateutil.parser import parse
# print(parse(tn.parse('3月26日晚20:00')['timestamp']))

string = '2021-02-28T20:27:33Z'[:-1]
print(parse(string))