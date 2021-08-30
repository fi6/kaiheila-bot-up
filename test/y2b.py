import sys
sys.path.append('.')

from configs import auth
from pyyoutube import Api


char = 'palutena'

api = Api(api_key=auth.y2b_api_key)
result = api.search(q='smash ultimate vs {} -amiibo'.format(char),
                    parts=['snippet'],
                    limit=50,
                    count=50,
                    order='date')
for item in result.items[:5]:
    print(item.to_dict())