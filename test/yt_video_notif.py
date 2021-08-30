import sys
sys.path.append('.')

import core
import asyncio
import functions
from functions import bot

# asyncio.get_event_loop().run_until_complete(core.polling.check_yt_video_task())
bot.run()
