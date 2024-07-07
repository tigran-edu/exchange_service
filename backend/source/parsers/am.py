from backend.source.parsers.basic import *
from backend.source.clients.selenium import SELENIUM_CLIENT
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from collections import defaultdict
import time


class ArdishBank(WebSite):
    def __init__(self):
        self.url = "https://ardshinbank.am/for_you/Artarjuyti-poxanakum?lang=ru"
        self.besnal_button_xpath = (
            '//*[@id="__nuxt"]/div/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]'
        )
        self.table_xpath = (
            '//*[@id="__nuxt"]/div/div/section[3]/div/div[1]/div[3]/table'
        )
        self.browser = SELENIUM_CLIENT

    async def handle(self) -> WebSiteResonse:
        logging.info("Handle start for ArdishBank")

        try:
            logging.info(f"Get request {self.url}")
            self.browser.get(self.url)
            time.sleep(1)
        except Exception as ex:
            logging.error(f"Get request failed {self.url}")
            return WebSiteResonse(return_code=StatusCode.GetError)

        try:
            logging.info("Click besnal button")
            WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.besnal_button_xpath))
            ).click()
        except Exception as ex:
            logging.error(f"Click besnal button failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.ClickError)

        try:
            logging.info("Find rates table")
            table = self.browser.find_element(By.XPATH, self.table_xpath).get_attribute(
                "innerHTML"
            )
        except Exception as ex:
            logging.error(f"Find rates table failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.GetTableError)

        return self.make_response(table)

    def make_response(self, table: str) -> WebSiteResonse:
        table_data = [
            [cell.text for cell in row("td")]
            for row in BeautifulSoup(table, "html.parser")("tr")
        ]

        logging.info(f"Table schema {table_data[0]}")
        table_dict = defaultdict(Exchange)
        try:
            rur_data, usd_data, eur_data = self.find_currency(
                table_data, ["RUR", "USD", "EUR"]
            )
            table_dict["USD"].buy = float(rur_data[1]) / float(usd_data[2])
            table_dict["USD"].sell = float(usd_data[1]) / float(rur_data[2])

            table_dict["EUR"].buy = float(rur_data[1]) / float(eur_data[2])
            table_dict["EUR"].sell = float(eur_data[1]) / float(rur_data[2])
        except Exception as ex:
            logging.error(f"Evaluation error: {ex}")
            return WebSiteResonse(return_code=StatusCode.EvaluationError)

        return WebSiteResonse(return_code=StatusCode.OK, rates=dict(table_dict))

    @staticmethod
    def find_currency(table, currencies):
        response = []
        for currency in currencies:
            for data in table:
                if currency in data:
                    response += [data]
                    break
        return response

class AmeriaBank(WebSite):
    def __init__(self):
        self.url = "https://ameriabank.am/ru/exchange-rates"
        self.table_xpath = (
            '//*[@id="dnn_ctr44240_View_grdRates"]'
        )
        self.browser = SELENIUM_CLIENT

    async def handle(self) -> WebSiteResonse:
        logging.info("Handle start for AmeriaBank")

        try:
            logging.info(f"Get request {self.url}")
            self.browser.get(self.url)
            time.sleep(1)
        except Exception as ex:
            logging.error(f"Get request failed {self.url}")
            return WebSiteResonse(return_code=StatusCode.GetError)

        try:
            logging.info("Find rates table")
            table = self.browser.find_element(By.XPATH, self.table_xpath).get_attribute(
                "innerHTML"
            )
        except Exception as ex:
            logging.error(f"Find rates table failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.GetTableError)

        return self.make_response(table)

    def make_response(self, table: str) -> WebSiteResonse:
        table_data = [
            [cell.text for cell in row("td")]
            for row in BeautifulSoup(table, "html.parser")("tr")
        ]

        logging.info(f"Table schema {table_data[0]}")
        table_dict = defaultdict(Exchange)
        try:
            rur_data, usd_data, eur_data = self.find_currency(
                table_data, ["RUB", "USD", "EUR"]
            )
            table_dict["USD"].buy = float(rur_data[3].replace(",", ".")) / float(usd_data[4].replace(",", "."))
            table_dict["USD"].sell = float(usd_data[3].replace(",", ".")) / float(rur_data[4].replace(",", "."))

            table_dict["EUR"].buy = float(rur_data[3].replace(",", ".")) / float(eur_data[4].replace(",", "."))
            table_dict["EUR"].sell = float(eur_data[3].replace(",", ".")) / float(rur_data[4].replace(",", "."))
        except Exception as ex:
            logging.error(f"Evaluation error: {ex}")
            return WebSiteResonse(return_code=StatusCode.EvaluationError)

        return WebSiteResonse(return_code=StatusCode.OK, rates=dict(table_dict))

    @staticmethod
    def find_currency(table, currencies):
        response = []
        for currency in currencies:
            for data in table:
                if currency in data:
                    response += [data]
                    break
        return response
