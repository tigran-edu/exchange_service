from backend.source.parsers.am import *
from backend.source.parsers.basic import WebSite
from typing import Collection


CONFIG = {"ARMENIA": [ArdishBank(), AmeriaBank(), HSBCBank(), AraratBank(), ConverseBank()]}


class ParserResonse:
    def __init__(self):
        pass


class Parser:
    @staticmethod
    async def pars(websites: Collection[WebSite]) -> ParserResonse:
        responses = []
        for website in websites:
            responses += [await website.handle()]
        return responses
