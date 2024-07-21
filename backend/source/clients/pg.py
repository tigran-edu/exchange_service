from psycopg2.extras import RealDictCursor
import psycopg2
import time
import os
import logging

_connection = None
PG_CLIENT = None


def try_connect():
    def connect():
        return psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )

    counter = 10
    conn = None
    while counter > 0:
        try:
            logging.info("Try to connect to the PostgreDB")
            conn = connect()
            break
        except Exception as ex:
            logging.warning(f"Connection failed due to exception: {ex}")
            counter -= 1
            time.sleep(10)
    if conn == None:
        raise Exception("Can not connect to the PG.")
    logging.info("Connection has been established")
    return conn


def create_pg_client():
    global PG_CLIENT
    _connection = try_connect()
    _connection.autocommit = True
    PG_CLIENT = _connection.cursor(cursor_factory=RealDictCursor)
    return PG_CLIENT


def close_client():
    global PG_CLIENT, _connection
    _connection.close()
    PG_CLIENT.close()
