import json
from typing import List
from models.__event import _Event


def event_entry_card(events: List[_Event]):
    event_cards = history_card(events)
    # TODO
    card = [{
        "type":
        "card",
        "theme":
        "secondary",
        "size":
        "lg",
        "modules": [{
            "type": "header",
            "text": {
                "type": "plain-text",
                "content": "活动菜单"
            }
        }, {
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "查询活动"
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type": "button",
                "theme": "primary",
                "value": ".活动 create",
                "click": "return-val",
                "text": {
                    "type": "plain-text",
                    "content": "创建新活动"
                }
            }]
        }]
    }, *event_cards]
    card_str = json.dumps(card)
    # print(card_str)
    return card_str


def history_card(events: List[_Event]):
    if not len(events):
        return []
    modules = [{
        "type": "header",
        "text": {
            "type": "plain-text",
            "content": "近期历史活动"
        }
    }]
    for event in events:
        event_sections = [{
            "type": "divider"
        }, {
            "type": "section",
            "text": {
                "type":
                "kmarkdown",
                "content":
                "**{title}**\n{time} {address}".format(
                    title=event.title,
                    time=event.start_time_str,
                    address=event.address.to_string())
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": ".菜单 活动 update {id}".format(id=event.pk),
                "text": {
                    "type": "plain-text",
                    "content": "修改"
                }
            }, {
                "type": "button",
                "theme": "primary",
                "value": ".菜单 活动 create {id}".format(id=event.pk),
                "click": "return-val",
                "text": {
                    "type": "plain-text",
                    "content": "创建并继承"
                }
            }]
        }]
        modules = [*modules, *event_sections]

    return [{
        "type": "card",
        "theme": "secondary",
        "size": "lg",
        "modules": modules
    }]
