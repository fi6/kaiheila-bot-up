from datetime import datetime
from enum import unique
from typing import List
from utils.date import get_time_str
from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import BooleanField, DateTimeField, DynamicField, EmbeddedDocumentField, ListField, StringField
from pyyoutube.models.video import Video


class MatchInfoDoc(EmbeddedDocument):
    title: str = StringField(required=True)
    match_name: str = StringField()
    p1: str = StringField()
    p1_fighter: List[str] = ListField(StringField(),
                                      default=[])  # fighter in code
    p2: str = StringField()
    p2_fighter: List[str] = ListField(StringField(), default=[])
    pool: bool = BooleanField()
    grand_final: bool = BooleanField()
    winner: bool = BooleanField()
    loser: bool = BooleanField()
    round: str = StringField()
    corrected: bool = BooleanField()


class YTVideo(Document):
    _raw = DynamicField()
    match_info = EmbeddedDocumentField(MatchInfoDoc)
    vid = StringField(required=True, unique=True)
    title = StringField(required=True)
    publish = DateTimeField(required=True)
    desc = StringField()
    channel_id: str = StringField(db_field='channelId')
    thumbnails: dict = DynamicField()
    pic: str = StringField()
    post: dict = DynamicField()
    reprint_bvid: str = StringField()
    channel_title = StringField(db_field='channelTitle')

    @property
    def thumbnail(self) -> str:
        for res in ['maxres', 'standard', 'high']:
            if self.thumbnails.get(res):
                return self.thumbnails[res]['url']
            return self.thumbnails['medium']['url']

    @property
    def pubdate_str(self) -> str:
        return get_time_str(self.publish if isinstance(self.publish, datetime)
                            else datetime.fromisoformat(self.publish[:-1]))

    @classmethod
    def from_item(cls, item: Video):
        new_doc = cls()
        new_doc._raw = item.to_dict()
        new_doc.vid = item.id
        new_doc.title = item.snippet.title
        new_doc.publish = item.snippet.publishedAt
        new_doc.desc = item.snippet.description
        new_doc.channel_id = item.snippet.channelId
        new_doc.thumbnails = item.snippet.thumbnails.to_dict()
        new_doc.channel_title = item.snippet.channelTitle
        return new_doc

    def update_from_item(self, item: Video):
        self._raw = item.to_dict()
        self.vid = item.id
        self.title = item.snippet.title
        self.publish = item.snippet.publishedAt
        self.desc = item.snippet.description
        self.channel_id = item.snippet.channelId
        self.thumbnails = item.snippet.thumbnails.to_dict()
        self.channel_title = item.snippet.channelTitle
        return self

    def update_match_info(self, parsed_info, corrected=False):
        self.match_info = MatchInfoDoc(corrected=corrected,
                                       **parsed_info.__dict__)
        self.save()

    def to_raw_card(self, cover: str):
        self.pic = cover
        return [{
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FF0000',
            "size":
            "sm",
            "modules": [{
                "type": "image-group",
                "elements": [{
                    "type": "image",
                    "src": self.pic,
                }]
            }]
        }, {
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FF0000',
            "size":
            "lg",
            "modules": [{
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "视频更新"
                }
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "**{title}**\n[YouTube链接]({url})".format(
                        url=f'https://www.youtube.com/watch?v={self.vid}',
                        title=self.title)
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type":
                    "kmarkdown",
                    "content":
                    "作者: {author}".format(author=self.channel_title)
                }]
            }, {
                "type":
                "context",
                "elements": [{
                    "type":
                    "kmarkdown",
                    "content":
                    "发布于：{pubdate}".format(pubdate=self.pubdate_str)
                }]
            }]
        }]

    def to_reprint_card(self):
        return [{
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FB7299',
            "size":
            "sm",
            "modules": [{
                "type": "image-group",
                "elements": [{
                    "type": "image",
                    "src": self.pic,
                }]
            }]
        }, {
            "type":
            "card",
            "theme":
            "info",
            'color':
            '#FB7299',
            "size":
            "lg",
            "modules": [{
                "type": "header",
                "text": {
                    "type": "plain-text",
                    "content": "视频搬运更新"
                }
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "**[{title}]({url})**".format(
                        url=
                        f'https://www.bilibili.com/video/{self.reprint_bvid}',
                        title=self.title)
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type":
                    "kmarkdown",
                    "content":
                    "搬运账号: [斗天堂](https://space.bilibili.com/645704621)"
                }]
            }, {
                "type": "divider"
            }, {
                "type": "section",
                "text": {
                    "type":
                    "kmarkdown",
                    "content":
                    "{desc}".format(desc=self.desc if len(self.desc) <= 152
                                    else self.desc[:150] + '...', )
                }
            }, {
                "type":
                "context",
                "elements": [{
                    "type":
                    "kmarkdown",
                    "content":
                    "发布于：{pubdate}".format(pubdate=self.pubdate_str)
                }]
            }]
        }]
