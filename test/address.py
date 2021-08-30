import sys
sys.path.append('.')

import cpca
import pandas

from models.__event import _Address

df: pandas.DataFrame = cpca.transform(['天津市'])
result = df.iloc[0].to_dict()
add = _Address(province=result['省'],
               city=result['市'],
               district=result.get('区'),
               detail=result.get('地址'),
               code=result['adcode'])

print(add.to_json())