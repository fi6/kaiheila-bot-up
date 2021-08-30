from models.group import CharGroup, GroupType, OfflineGroup
from typing import Dict, List, Tuple
from models import Group


def get_group_card():
    offline_group_dict = get_offline_groups()
    modules = []
    for key, item in offline_group_dict.items():
        modules.append({
            "type": "header",
            "text": {
                "type": "plain-text",
                "content": key
            }
        })
        for group in item:
            modules.append({
                "type": "section",
                "text": {
                    "type": "kmarkdown",
                    "content": '{name}\n'
                }
            })
    return [{
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": modules
    }]


def get_offline_groups() -> Dict[str, List[OfflineGroup]]:

    offline_groups = OfflineGroup.objects().order_by('address.code')
    offline_group_dict = {}
    for group in offline_groups:
        greater_area = group.address._greater_admin_area
        if offline_group_dict.get(greater_area):
            offline_group_dict[greater_area] = [
                *offline_group_dict[greater_area], group
            ]
        else:
            offline_group_dict[greater_area] = [group]
    return offline_group_dict


def get_char_groups() -> List[CharGroup]:
    return list(CharGroup.objects().order_by('name'))
