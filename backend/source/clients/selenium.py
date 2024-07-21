from selenium import webdriver
import time
import logging


SELENIUM_CLIENT = None


def try_connect():
    counter = 10
    conn = None
    options = webdriver.ChromeOptions()
    while counter > 0:
        try:
            logging.info("Try to connect to the Selenium")
            conn = webdriver.Remote(
                command_executor="http://selenium:4444/wd/hub", options=options
            )
            break
        except Exception as ex:
            logging.info(f"Connection failed due to {ex}")
            counter -= 1
            time.sleep(10)
    if conn == None:
        raise Exception("Can not connect to the browser.")
    logging.info("Conection has been established")
    return conn


def create_client():
    global SELENIUM_CLIENT
    SELENIUM_CLIENT = try_connect()
    return SELENIUM_CLIENT


def close_client():
    global SELENIUM_CLIENT
    SELENIUM_CLIENT.quit()
