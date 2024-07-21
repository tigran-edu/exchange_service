import backend.source.sql as sql
from backend.source.schema import Tables
from backend.source.parsers.basic import WebSiteResonse
from typing import Collection
import logging


def create_rates_schema(schema_name: str, cursor):
    logging.info(f"Creating schema {schema_name}")
    cursor.execute(sql.CREATE_SCHEMA.format(schema_name))


def create_rates_table(table_name: str, cursor):
    logging.info(f"Creating table {table_name}")
    table = Tables.tables["rates"]
    cursor.execute(sql.CREATE_TABLE.format(table_name, table.get_schema()))


def delete_table(table_name: str, cursor):
    logging.info(f"Deleting table {table_name}")
    cursor.execute(sql.DELETE_TABLE.format(table_name))


def get_rates_from_db(table_name: str, cursor):
    logging.info("Get rates from db table_name")
    _, country = table_name.split(".")
    query = sql.GET_RATES.format(table_name, 5)
    logging.info(f"SQL QUERY {query}")
    cursor.execute(query)
    return cursor.fetchall()


def write_rates_to_db(table_name: str, responses: Collection[WebSiteResonse], cursor):
    if len(responses) == 0:
        logging.warning("Responses are empty")
        return
    values = ", ".join([f"(DEFAULT, {str(resp)})" for resp in responses])
    logging.info(f"New rates\n{values}")
    query = sql.INSERT_NEW_RATES.format(
        table_name, Tables.tables["rates"].get_fields(), values
    )
    logging.info(f"SQL QUERY {query}")
    cursor.execute(query)
