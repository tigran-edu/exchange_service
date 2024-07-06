import backend.source.sql as sql
from backend.source.schema import Tables
import uuid
from datetime import datetime
from hashlib import md5
import jwt
import logging
import re

def get_user(login, cursor):
    cursor.execute(sql.SELECT_USER.format(login))
    return cursor.fetchone()


def get_user_login(user_id, cursor):
    cursor.execute(sql.SELECT_USER_LOGIN.format(user_id))
    return cursor.fetchone()


def get_post(post_id, cursor):
    cursor.execute(sql.SELECT_POST.format(post_id))
    return cursor.fetchone()


def create_table(table_name: str, cursor):
    table = Tables.tables[table_name]
    cursor.execute(sql.CREATE_TABLE.format(table_name, table.get_schema()))


def delete_table(table_name: str, cursor):
    cursor.execute(sql.DELETE_TABLE.format(table_name))


def is_uuid(user_id):
    UUID_PATTERN = re.compile(
        r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE
    )
    return bool(UUID_PATTERN.match(user_id))


def change_user_data(data, login, cursor):
    new_set = []
    if data.first_name:
        new_set += [f"first_name = '{data.first_name}'"]
    if data.second_name:
        new_set += [f"second_name = '{data.second_name}'"]
    if data.email:
        new_set += [f"email = '{data.email}'"]
    if data.phone_number:
        new_set += [f"phone_number = '{data.phone_number}'"]
    if data.birth_day:
        new_set += [f"birth_day = '{data.birth_day}'"]
    cursor.execute(sql.UPDATE_USER.format(", ".join(new_set), login))

