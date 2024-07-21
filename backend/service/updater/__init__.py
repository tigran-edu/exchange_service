import logging
import asyncio
import sys
import inspect
import backend.source.clients.pg as pg
import backend.source.clients.selenium as selenium
import backend.source.scripts as scripts
from backend.source.clients.parser import Parser
from backend.source.parsers.basic import StatusCode
from backend.source.parsers.am import *
from collections import defaultdict

COUNTRIES = ["am"]
SCHEMA_NAME = "rates"
CONFIG = defaultdict(list)


def init_tables(pg_client):
    logging.info(f"Creating {SCHEMA_NAME}")
    scripts.create_rates_schema(SCHEMA_NAME, pg_client)
    for country in COUNTRIES:
        scripts.create_rates_table(f"{SCHEMA_NAME}.{country}", pg_client)

def init_config():
    logging.info("INIT CONFIG")
    global CONFIG
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and "Bank" in name:
            country = str(obj).split('.')[-2]
            logging.info(f"Country: {country}, Bank: {name}")
            CONFIG[country].append(obj())



async def update_rates(pg_client):
    for country in COUNTRIES:
        responses = await Parser.pars(CONFIG[country])
        responses = [resp for resp in responses if resp.return_code == StatusCode.OK]
        scripts.write_rates_to_db(f"{SCHEMA_NAME}.{country}", responses, pg_client)


async def main():
    pg_client = pg.create_client()
    selenium.create_client()
    init_tables(pg_client)
    init_config()
    await update_rates(pg_client)
    pg.close_client()
    selenium.close_client()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
