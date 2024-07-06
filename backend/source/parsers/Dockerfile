FROM python:latest

RUN pip install requests
RUN pip install bs4
RUN pip install selenium

RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv /chromedriver /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

RUN apt-get install chromium-browser

COPY ./ ./

ENTRYPOINT python -u test.py
