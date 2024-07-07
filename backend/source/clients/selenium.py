from selenium import webdriver
import time

def try_connect():
    counter = 10
    conn = None
    options = webdriver.ChromeOptions()
    while counter > 0:
        try:
            conn = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", options=options)
            break
        except Exception:
            counter -= 1
            time.sleep(10)
    if conn == None:
        raise Exception("Can not connect to the PG.")
    return conn

SELENIUM_CLIENT = try_connect()