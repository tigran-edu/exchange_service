import abc
import time
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
    GetTableError = 2
    EvaluationError = 3


class WebSiteResonse:
    def __init__(
        self, return_code: StatusCode, bank: str, rates: Optional[dict] = None
    ):
        self.return_code = return_code
        self.rates = rates
        self.bank = bank
        self.timestamp = int(time.time())

    def __str__(self):
        if self.rates is None:
            raise Exception("No rates.")
        return f"'{self.bank}', {self.timestamp}, {self.rates['EUR'].sell}, {self.rates['USD'].sell}, {self.rates['EUR'].buy}, {self.rates['USD'].buy}"


class WebSite:
    url: str
    bank: str
    currencies = ["USD", "EUR", "RUR"]

    @abc.abstractmethod
    async def handle(self, html) -> WebSiteResonse:
        pass

    @abc.abstractmethod
    def make_response(self, table: str) -> WebSiteResonse:
        pass

    @staticmethod
    def find_currency(table, currencies):
        response = []
        for currency in currencies:
            for data in table:
                if currency in data:
                    response += [data]
                    break
        return response