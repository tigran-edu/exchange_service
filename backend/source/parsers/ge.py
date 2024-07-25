import backend.source.clients.selenium as selenium
from backend.source.parsers.basic import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import logging
from collections import defaultdict
import time


class CartuBank(WebSite):
    def __init__(self):
        self.url = "https://www.cartubank.ge/?lng=eng"
        self.bank = "Cartubank"
        self.table_name= "currency-rates"
        self.browser = selenium.SELENIUM_CLIENT

    async def handle(self) -> WebSiteResonse:
        logging.info(f"Handle start for {self.bank}")

        try:
            logging.info(f"Get request {self.url}")
            self.browser.get(self.url)
            time.sleep(1)
        except Exception as ex:
            logging.error(f"Get request failed {self.url}\nError: {ex}")
            return WebSiteResonse(return_code=StatusCode.GetError, bank=self.bank)

        try:
            logging.info("Find rates table")
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            table = soup.find("div", {"class": self.table_name,})
            table = [div.text.strip() for div in table.find_all('div')][::5]
            table = [row.split() for row in table]
        except Exception as ex:
            logging.error(f"Find rates table failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.GetTableError, bank=self.bank)

        return self.make_response(table)

    def make_response(self, table_data: str) -> WebSiteResonse:
        logging.info(f"Table {table_data}")
        table_dict = defaultdict(Exchange)
        try:
            rur_data, usd_data, eur_data = self.find_currency(
                table_data, ["RUB", "USD", "EUR"]
            )
            table_dict["USD"].sell = float(usd_data[2]) / float(rur_data[1])
            table_dict["USD"].buy = float(usd_data[1]) / float(rur_data[2])

            table_dict["EUR"].sell = float(eur_data[2]) / float(rur_data[1])
            table_dict["EUR"].buy = float(eur_data[1]) / float(rur_data[2])
        except Exception as ex:
            logging.error(f"Evaluation error: {ex}")
            return WebSiteResonse(
                return_code=StatusCode.EvaluationError, bank=self.bank
            )

        return WebSiteResonse(
            return_code=StatusCode.OK, bank=self.bank, rates=dict(table_dict)
        )

class SwissCapitalBank(WebSite):
    def __init__(self):
        self.url = "https://swisscapital.ge/en/currency"
        self.bank = "SwissCapital"
        self.table_xpath = '/html/body/div[1]/header[2]/div[3]/div/div[1]/div[1]/table/tbody'
        self.browser = selenium.SELENIUM_CLIENT

    async def handle(self) -> WebSiteResonse:
        logging.info(f"Handle start for {self.bank}")

        try:
            logging.info(f"Get request {self.url}")
            self.browser.get(self.url)
            time.sleep(1)
        except Exception as ex:
            logging.error(f"Get request failed {self.url}")
            return WebSiteResonse(return_code=StatusCode.GetError, bank=self.bank)

        try:
            logging.info("Find rates table")
            table = self.browser.find_element(By.XPATH, self.table_xpath).get_attribute(
                "innerHTML"
            )
        except Exception as ex:
            logging.error(f"Find rates table failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.GetTableError, bank=self.bank)

        return self.make_response(table)

    def make_response(self, table: str) -> WebSiteResonse:
        table_data = [
            [cell.text for cell in row("td")]
            for row in BeautifulSoup(table, "html.parser")("tr")
        ]

        logging.info(f"Table {table_data}")
        table_dict = defaultdict(Exchange)
        try:
            rur_data, usd_data, eur_data = self.find_currency(
                table_data, ["RUB", "USD", "EUR"]
            )
            table_dict["USD"].sell = round(float(usd_data[4].replace(",", "."))/ float(rur_data[3].replace(",", ".")), 2)
            table_dict["USD"].buy = round(float(usd_data[3].replace(",", ".")) / float(rur_data[4].replace(",", ".")), 2)

            table_dict["EUR"].sell = round(float(eur_data[4].replace(",", "."))/ float(rur_data[3].replace(",", ".")), 2)
            table_dict["EUR"].buy = round(float(eur_data[3].replace(",", ".")) / float(rur_data[4].replace(",", ".")), 2)
        except Exception as ex:
            logging.error(f"Evaluation error: {ex}")
            return WebSiteResonse(
                return_code=StatusCode.EvaluationError, bank=self.bank
            )

        return WebSiteResonse(
            return_code=StatusCode.OK, bank=self.bank, rates=dict(table_dict)
        )