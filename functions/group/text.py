from models.group import GeneralGroup, OtherGroup
from .list import get_offline_groups, get_char_groups


def get_group_passage():
    text = ''
    offline_groups = get_offline_groups()
    text += '## 线下群'
    for key, groups in offline_groups.items():
        text += f'\n\n### {key}'
        for group in groups:
            text += (f'\n\n**{group.name}**  ' +
                     f'\n加群方式：{group.join_type.to_string()} {group.contact}  ')
            if group.address.detail:
                text += f'\n活动地址：{group.address.to_string()}  '
            if group.remark:
                text += f'\n备注：{group.remark}  '

    group = None
    text += '\n\n## 角色群'
    for group in get_char_groups():
        text += (f'\n\n**{group.name}**  ' +
                 f'\n加群方式：{group.join_type.to_string()} {group.contact}  ')
        if group.remark:
            text += f'\n备注：{group.remark}  '

    group = None
    text += '\n\n## 综合群'
    for group in GeneralGroup.objects():
        text += (f'\n\n**{group.name}**  ' +
                 f'\n加群方式：{group.join_type.to_string()} {group.contact}  ')
        if group.remark:
            text += f'\n备注：{group.remark}  '

    group = None
    text += '\n\n## 其他群聊'
    for group in OtherGroup.objects():
        text += (f'\n\n**{group.name}**  ' +
                 f'\n加群方式：{group.join_type.to_string()} {group.contact}  ')
        if group.remark:
            text += f'\n备注：{group.remark}  '

    text += '\n---\n\n以上收录了近期补全了信息、已加入数据库的群聊，你还可以尝试[查看旧的群聊汇总](https://weibo.com/ttarticle/p/show?id=2309404503596933709905)以查看更多地区的线下群。  \n\n如果想把你的群加入汇总，或推荐某个群，请私聊我进行更新。'

    with open('output.md', 'w') as file:
        file.write(text)
