from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from am import AmeriaBank
import asyncio
import logging


async def main():
    rates = await AmeriaBank().handle()
    for key, value in rates.rates.items():
        print(f"currency {key}", value)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
