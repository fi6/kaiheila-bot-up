from abc import ABC, abstractmethod
from typing import List
from khl import Command
from khl.message import Msg


class MyCommand(Command, ABC):
    trigger: List[str]

    def __init__(self):
        pass

    @abstractmethod
    async def execute(self, msg: Msg, *args: str):
        pass
