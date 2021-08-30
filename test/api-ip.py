import requests
import sys
import socket
sys.path.append('.')

# ips = socket.gethostbyname_ex('api.live.bilibili.com')
# print(ips[2])

url = 'http://148.153.64.18/room/v1/Room/getRoomInfoOld'

headers = {
    'Host': 'api.live.bilibili.com',
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.47 Safari/537.36 Edg/89.0.774.27",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.bilibili.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}

result = requests.get(url, {'mid': 9409346}, headers=headers)
print(result.json()['data'])
