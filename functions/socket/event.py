from typing import List
from .._instance import sio


@sio.event
def register_event(sid, data):
    id: str = data['id']
    args: List[str] = data['args']
