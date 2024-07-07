FROM python:latest

ENV SERVICE_DIR=/backend

COPY $SERVICE_DIR/requirements.txt ./
RUN pip3 install setuptools --upgrade
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


RUN apt-get update
RUN apt-get install libnss3

RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

COPY ./ ./

ENV PYTHONPATH "${PYTHONPATH}:$SERVICE_DIR"

RUN echo $SERVICE_DIR

# ENTRYPOINT python -u $SERVICE_DIR/service/__init__.py
ENTRYPOINT chromedriver --version
