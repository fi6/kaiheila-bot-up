from dataclasses import dataclass, fields


@dataclass
class UserVideo():
    bvid: str
    title: str
    play: int
    author: str
    mid: int
    created: int
    length: str
    aid: int
    description: str
    pic: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)
