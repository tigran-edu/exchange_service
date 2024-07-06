import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome(service=webdriver.ChromeService(executable_path='/opt/homebrew/bin/chromedriver'))



url = "https://ardshinbank.am/?lang=ru"

browser.get(url)
time.sleep(5)
besnal = browser.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/section[8]/div/div[1]/div[2]/div/div[2]/div[2]')
besnal.click()

time.sleep(100)

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}


resp = requests.get(url, headers=headers)

html = resp.text
soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())


