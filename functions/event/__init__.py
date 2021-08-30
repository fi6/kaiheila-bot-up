import json
from typing import List

import configs

from cacheout import LRUCache

import core
from khl.message import Msg
from models.__event import OfflineEvent, _Address, _Event

from .._command import MyCommand
from ..cards.event_entry import event_entry_card

cache = LRUCache(maxsize=0, ttl=300)


class EventEntry(MyCommand):
    trigger = ['活动']

    async def execute(self, msg: Msg, *args: str):
        if not len(args):
            return await self.entry(msg)
        if args[0] == 'update' and len(args) == 2:
            return await self.update(msg, args[1])
        if args[0] == 'create' and len(args) == 1:
            return await self.create(msg)
        if args[0] == 'create' and len(args) == 2:
            return await self.create_from(msg, args[1])

    async def entry(self, msg: Msg):
        """
        shows history events(max 3), buttons(new)
        """
        recent_events: List[_Event] = _Event.objects().order_by('-start')[:5]
        await msg.ctx.send_card_temp(event_entry_card(recent_events))

    async def review(self, msg: Msg, id: str):
        pass

    async def update(self, msg: Msg, id: str):
        try:
            event = _Event.objects.get(id=id)
            await msg.ctx.send_card_temp()
            input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
            if not input.content:
                raise ValueError('没有收到有效的收入')

        except ValueError as e:
            await msg.ctx.send_temp(str(e.args[0]))

    async def create_from(self, msg: Msg, id: str):
        pass

    async def create(self, msg: Msg):
        event = OfflineEvent(user=msg.ctx.user_id)
        parsed_event = core.event.event_parser(event, text='1')
        # if cache.get(msg.ctx.user_id):
        #     event = cache.get(msg.ctx.user_id)
        #     cache.set(msg.ctx.user_id, event)
        # else:
        #     event = OfflineEvent(user=msg.ctx.user_id)
        #     cache.set(msg.ctx.user_id, event)

        # try:
        #     if not event.title:
        #         await self.input_title(msg, event)
        #     if not event.start:
        #         await self.input_start_time(msg, event)
        #     if not event.contact:
        #         await self.input_contact(msg, event)
        #     if not event.register:
        #         await self.input_register(msg, event)
        #     if not event.info:
        #         await self.input_info(msg, event)
        #     if not event.fee:
        #         await self.input_fee(msg, event)
        #     if not event.address.code:
        #         await self.input_address(msg, event)
        #         await self.input_series(msg, event)
        #         await self.input_live(msg, event)
        # except ValueError:
        #     return await msg.ctx.send_temp('输入超时或输入有误，请点击按钮以从上一步开始')

        event.save()
        await msg.ctx.send_card_temp(event.to_card())
        await msg.ctx.send_temp('输入已完成，以上是你的活动信息预览。如果确定发布，请发送`是`，否则请发送`否`')

        result = await msg.ctx.wait_user(msg.ctx.user_id)
        if result.content == '是':
            sent = await msg.ctx.bot.send(configs.channel.notif,
                                          event.to_card(),
                                          type=10)
            event.publish = sent['msg_id']
            event.save()
        elif result.content == '否':
            pass

    async def input_title(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动标题（以下全部输入60秒内有效，超时需重新开始）')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        event.title = input.content
        return input.content

    async def input_start_time(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动开始时间，尽量保持格式为x月x日xx:xx')
        while True:
            input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
            if not input.content:
                raise ValueError()
            result = get_time(input.content)
            if result:
                event.start = result
                return result
            else:
                await msg.ctx.send_temp('无法解析时间。请输入活动开始时间，保持格式为x月x日xx:xx')
                return None

    async def input_contact(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动联系方式，如：QQ群xxxxx')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        event.contact = input.content
        return input.content

    async def input_register(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动报名方式，如：QQ群内报名 或 http://smash.gg/xxxxx')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        event.register = input.content
        return input.content

    async def input_info(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动描述，如：北京周赛，8点开始单打比赛，有双打')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        event.info = input.content
        return input.content

    async def input_fee(self, msg: Msg, event: OfflineEvent):
        await msg.ctx.send_temp('请输入活动费用，如：单打20元，双打免费')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        event.fee = input.content

    async def input_address(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('请输入活动地址，如：xx市xx区xxx大楼xx号\n系统将自动解析地址。')
        while True:
            input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
            if not input.content:
                raise ValueError()
            result = get_address(input.content)
            if result:
                event.address = result
                break
            else:
                await msg.ctx.send_temp(
                    '无法解析地址，请重新输入。\n请尽量输入完整地址，如`北京市东城区方家胡同12号野友趣`')

    async def input_series(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('是否为系列活动？如果是，请为系列活动创建代号（如：szweeklys3），不是请输入`否`'
                                )
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        if input.content == '否':
            event.series = False
        else:
            event.series = True
            event.code = input.content

    async def input_live(self, msg: Msg, event: _Event):
        await msg.ctx.send_temp('是否有线上直播？如果有，请输入直播间地址，否则请输入`否`')
        input = await msg.ctx.wait_user(msg.ctx.user_id, 60)
        if not input.content:
            raise ValueError()
        if input.content == '否':
            pass
        else:
            event.live = input.content
