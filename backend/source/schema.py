from datetime import datetime


class Schema:
    keys = []
    schema = {}

    @classmethod
    def get_schema(cls):
        schema = ", ".join([f"{k} {v}" for k, v in cls.schema.items()])
        if cls.keys:
            schema += f", PRIMARY KEY({cls.get_keys()})"
        return schema

    @classmethod
    def get_keys(cls):
        return " ,".join(cls.keys)

    @classmethod
    def get_fields(cls):
        return " ,".join(list(cls.schema.keys()))


class ExchangeRateSchema(Schema):
    keys = ["id"]
    schema = {
        "id": "serial",
        "bank": "text",
        "update_time": "bigint",
        "SELL_EUR": "double precision",
        "SELL_USD": "double precision",
        "BUY_EUR": "double precision",
        "BUY_USD": "double precision",
    }


class Tables:
    tables = {"rates": ExchangeRateSchema}
