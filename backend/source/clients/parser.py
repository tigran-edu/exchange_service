from backend.source.parsers.am import *
from backend.source.parsers.basic import WebSite
from typing import Collection


CONFIG = {"ARMENIA": [ArdishBank(), AmeriaBank()]}


class ParserResonse:
    def __init__(self):
        pass


async def await_tasks(tasks):
    response = []
    for task in tasks:
        response.append(await task)
    return response


class Parser:
    @staticmethod
    async def pars(websites: Collection[WebSite]) -> ParserResonse:
        tasks = []
        for website in websites:
            tasks += [website.handle()]
        return await await_tasks(tasks)
