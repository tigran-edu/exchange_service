import backend.source.clients.selenium as selenium
from backend.source.parsers.basic import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from collections import defaultdict
import time


class ArdishBank(WebSite):
    def __init__(self):
        self.url = "https://ardshinbank.am/for_you/Artarjuyti-poxanakum?lang=ru"
        self.bank = "Ardshinbank"
        self.besnal_button_xpath = (
            "/html/body/div[1]/div/div/section[3]/div/div[1]/div[2]/div/div[2]"
        )
        self.table_xpath = (
            "/html/body/div[1]/div/div/section[3]/div/div[1]/div[3]/table"
        )
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
            logging.info("Click besnal button")
            WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.besnal_button_xpath))
            ).click()
        except Exception as ex:
            logging.error(f"Click besnal button failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.ClickError, bank=self.bank)

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
                table_data, ["RUR", "USD", "EUR"]
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


class AmeriaBank(WebSite):
    def __init__(self):
        self.url = "https://ameriabank.am/ru/exchange-rates"
        self.bank = "Ameriabank"
        self.table_xpath = '//*[@id="dnn_ctr44240_View_grdRates"]'
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
            table_dict["USD"].sell = float(usd_data[4].replace(",", ".")) / float(
                rur_data[3].replace(",", ".")
            )
            table_dict["USD"].buy = float(usd_data[3].replace(",", ".")) / float(
                rur_data[4].replace(",", ".")
            )

            table_dict["EUR"].sell = float(eur_data[4].replace(",", ".")) / float(rur_data[3].replace(",", "."))

            table_dict["EUR"].buy = float(eur_data[3].replace(",", ".")) / float(
                rur_data[4].replace(",", ".")
            )
        except Exception as ex:
            logging.error(f"Evaluation error: {ex}")
            return WebSiteResonse(
                return_code=StatusCode.EvaluationError, bank=self.bank
            )

        return WebSiteResonse(
            return_code=StatusCode.OK, bank=self.bank, rates=dict(table_dict)
        )


class HSBCBank(WebSite):
    def __init__(self):
        self.url = "https://www.hsbc.am/en-am/help/rates/"
        self.bank = "HSBC"
        self.table_xpath = (
            "/html/body/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div/table/tbody"
        )
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


class AraratBank(WebSite):
    def __init__(self):
        self.url = "https://www.araratbank.am/en/"
        self.bank = "AraratBank"
        self.table_xpath = "/html/body/main/div[2]/div/div/div[3]/div/div/div/div[2]/div[1]/div/div/table"
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


class ConverseBank(WebSite):
    def __init__(self):
        self.url = "https://conversebank.am/ru/"
        self.bank = "ConverseBank"
        self.besnal_button_xpath = "/html/body/div[2]/div/div[2]/div[4]/div/div[1]/div/div/div[2]/div[2]/button[2]"
        self.table_xpath = (
            "/html/body/div[2]/div/div[2]/div[4]/div/div[1]/div/div/div[2]/table"
        )
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
            logging.info("Click besnal button")
            WebDriverWait(self.browser, 20).until(
                EC.element_to_be_clickable((By.XPATH, self.besnal_button_xpath))
            ).click()
        except Exception as ex:
            logging.error(f"Click besnal button failed: {ex}")
            return WebSiteResonse(return_code=StatusCode.ClickError, bank=self.bank)

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
