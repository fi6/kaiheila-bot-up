import logging
from .._command import MyCommand
from khl import Msg
import core
from core.__video.__char import get_name_by_code


class VideoReprint(MyCommand):
    trigger = ['转载']

    async def execute(self, msg: Msg, *args: str):
        if not len(args):
            raise ValueError('no args given')
        if args[0] == 'y2b':
            id = core.api.youtube.get_id(
                args[1]) if '/' in args[1] else args[1]
            try:
                info, vid_doc = await self.confirm_info(msg, id)
                await msg.ctx.send_temp('确认完成，正在下载视频，通常需要2-5分钟……')
                files = core.video.yt_download(id)
                vid_path = files['video']
                cover_path = files['cover']
                await msg.ctx.send_temp('下载成功，正在投稿中……')
                char_list = [
                    get_name_by_code(code)
                    for code in [*info.p1_fighter, *info.p2_fighter]
                ]
                char_list = list(filter(None, char_list))
                result = await core.api.bilibili.submit_video(
                    info.format_title, char_list, id, vid_doc.desc, vid_path,
                    cover_path)
                await msg.ctx.send(
                    '(met){}(met)视频转载成功，bvid为：{}。审核结束后会发送视频更新推送。'.format(
                        msg.ctx.user.id, result['bvid']))
            except ValueError as e:
                await msg.ctx.send_temp('出现错误：{}\n请重新开始'.format(e.args[0]))
            except Exception as e:
                logging.exception(e)
                await msg.ctx.send_temp('出现未知错误，请截图给冰飞：\n{}'.format(e))

    async def confirm_info(self, msg: Msg, id: str):
        vid_docs = await core.api.youtube.save_videos(id)
        if not vid_docs or not len(vid_docs):
            raise ValueError('没有获取到视频信息，请检查视频是否存在')
        # parse info from title
        vid_doc = vid_docs[0]
        parsed_info = core.video.match_parser.parse(vid_doc.title)
        if not parsed_info:
            raise ValueError('解析视频信息失败，未收到视频标题')
        await msg.ctx.send_temp(
            '原视频标题：{}\n识别到的信息如下，请检查并发送确认后的信息文字(2分钟有效)\n{}'.format(
                vid_doc.title, parsed_info.to_string()))
        # confirm info with user
        input = await msg.ctx.wait_user(user_id=msg.ctx.user.id, timeout=120)
        if not input:
            raise ValueError('未收到输入')

        while input.content != parsed_info.to_string():
            parsed_info.from_string(input.content)  # modify self
            await msg.ctx.send_temp(
                '检测到修改，新识别的信息如下，请再次确认（主要是角色）后发送\n{}'.format(
                    parsed_info.to_string()))
            input = await msg.ctx.wait_user(user_id=msg.ctx.user.id,
                                            timeout=60)
            if not input:
                raise ValueError('未收到输入')
        # input.content == parsed_info.to_string()
        # parsed_info_doc = MatchInfoDoc(corrected=True, **parsed_info.__dict__)
        vid_doc.update_match_info(parsed_info, corrected=True)
        return parsed_info, vid_doc
