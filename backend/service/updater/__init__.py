import logging
import asyncio
import backend.source.clients.pg as pg
import backend.source.clients.selenium as selenium
import backend.source.scripts as scripts
from backend.source.clients.parser import Parser
from backend.source.parsers.basic import StatusCode
from backend.source.parsers import get_all_banks

COUNTRIES = ["am"]
SCHEMA_NAME = "rates"


def init_tables(pg_client):
    logging.info(f"Creating {SCHEMA_NAME}")
    scripts.create_rates_schema(SCHEMA_NAME, pg_client)
    for country in COUNTRIES:
        scripts.create_rates_table(f"{SCHEMA_NAME}.{country}", pg_client)


async def update_rates(pg_client):
    banks = get_all_banks()
    for country in COUNTRIES:
        responses = await Parser.pars(banks[country])
        responses = [resp for resp in responses if resp.return_code == StatusCode.OK]
        scripts.write_rates_to_db(f"{SCHEMA_NAME}.{country}", responses, pg_client)


async def main():
    pg_client = pg.create_client()
    selenium.create_client()
    init_tables(pg_client)
    await update_rates(pg_client)
    pg.close_client()
    selenium.close_client()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
