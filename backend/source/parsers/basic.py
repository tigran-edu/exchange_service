import requests
from bs4 import BeautifulSoup
import abc
from typing import Collection


class WebSite:
    url: str

    @abc.abstractmethod
    def handle(self, html):
        pass


class ParserResonse:
    def __init__(self):
        pass


class Parser:
    @abc.abstractmethod
    @staticmethod
    def pars(websites: Collection[WebSite]) -> ParserResonse:
        pass
