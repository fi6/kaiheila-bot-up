import json
from models import _Event


def raw_event_card(event: _Event):
    return json.dumps([{
        "type":
        "card",
        "theme":
        "secondary",
        "size":
        "lg",
        "modules": [{
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "目前的活动信息如下，请复制并进行修改，然后点击按钮再输入更新后的信息。"
            }
        }, {
            "type":
            "action-group",
            "elements": [{
                "type": "button",
                "click": "return-val",
                "theme": "primary",
                "value": "ok",
                "text": {
                    "type": "plain-text",
                    "content": "输入更新后的活动信息"
                }
            }]
        }]
    }, {
        "type":
        "card",
        "theme":
        "secondary",
        "size":
        "lg",
        "modules": [{
            "type": "section",
            "text": {
                "type": "kmarkdown",
                "content": "{event}".format(event=event.to_raw_info())
            }
        }]
    }])
