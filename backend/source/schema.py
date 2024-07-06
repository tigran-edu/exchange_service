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
    keys = ["bank_id"]
    schema = {
        "bank_id": "uuid",
        "bank_name": "text",
        "link": "text",
        "eur/rub": "float",
        "usd/rub": "float",
        "rub/eur": "float",
        "rub/usd": "float",
    }


class Tables:
    tables = {"exchange_rates": ExchangeRateSchema}
