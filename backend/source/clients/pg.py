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
            conn = connect()
            break
        except Exception:
            counter -= 1
            time.sleep(10)
    if conn == None:
        raise Exception("Can not connect to the PG.")
    return conn


def create_pg_client():
    _connection = try_connect()
    _connection.autocommit = True
    PG_CLIENT = _connection.cursor(cursor_factory=RealDictCursor)


def close_client():
    _connection.close()
    PG_CLIENT.close()
