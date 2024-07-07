FROM python:latest

ENV SERVICE_DIR=/backend

COPY $SERVICE_DIR/requirements.txt ./

RUN pip3 install setuptools --upgrade
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./ ./

ENV PYTHONPATH "${PYTHONPATH}:$SERVICE_DIR"

RUN echo $SERVICE_DIR

ENTRYPOINT python -u $SERVICE_DIR/service/__init__.py