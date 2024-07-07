import abc
from enum import IntEnum
from typing import Optional


class Exchange:
    buy: float
    sell: float

    def __str__(self):
        return f"buy: {self.buy} | sell: {self.sell}"


class StatusCode(IntEnum):
    OK = 0
    GetError = 1
    ClickError = 2
    GetTableError = 3
    EvaluationError = 4


class WebSiteResonse:
    def __init__(self, return_code: StatusCode, rates: Optional[dict]):
        self.return_code = return_code
        self.rates = rates


class WebSite:
    url: str
    currencies = ["USD", "EUR", "RUR"]

    @abc.abstractmethod
    async def handle(self, html) -> WebSiteResonse:
        pass

    @abc.abstractmethod
    def make_response(self, table: str) -> WebSiteResonse:
        pass
