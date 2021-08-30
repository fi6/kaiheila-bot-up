import re
from khl.message import TextMsg
from ._entry import BotEntry
from ._instance import bot, sio  # noqa
from .event import EventEntry
from . import notification  # noqa
from .video import video_entry
from utils import link_parser

bot_entry = BotEntry(EventEntry(), video_entry)
bot.add_command(bot_entry)


@bot.on_text_msg
async def entry(msg: TextMsg):
    if '2114466526' in msg.mention and len(
            msg.mention) == 1 and msg.content.startswith('@'):
        args = msg.content.split()
        if not len(args) > 1:
            return
        args = args[1:]
        await bot_entry.execute(msg, *args)
    elif link_parser(msg.content, scheme_only=True) and re.search(
            'bilibili', msg.content):
        parse_result = link_parser(msg.content)
        if not parse_result:
            return
        await video_entry.add(msg, [parse_result])
