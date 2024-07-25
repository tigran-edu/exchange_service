import logging
from fastapi import Depends, Body, Cookie, Response, Request, APIRouter
import backend.source.clients.pg as pg
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import backend.source.scripts as scripts
from backend.source.parsers import get_all_countries
import logging
import copy


router = APIRouter()
templates = Jinja2Templates(directory="/frontend")

COUNTRIES = {
    "am": "Armenia",
    "ge": "Georgia",
    "kg": "Kyrgyzstan",
    "rs": "Serbia",
    "tr": "Turkey",
    "uz": "Uzbekistan",
    "by": "Belarus"
}


def round_rates(rates):
    round_rates = copy.deepcopy(rates)
    for rate in round_rates:
        rate['sell_eur'] = str(round(float(rate['sell_eur']), 2))
        rate['sell_usd'] = str(round(float(rate['sell_usd']), 2))
        rate['buy_eur'] = str(round(float(rate['buy_eur']), 2))
        rate['buy_usd'] = str(round(float(rate['buy_usd']), 2))
    return round_rates


def tech_rates(rates):
    rates = copy.deepcopy(rates)
    for rate in rates:
        rate['sell_eur'] = str(1 / float(rate['sell_eur']))
        rate['sell_usd'] = str(1 / float(rate['sell_usd']))
    return rates



@router.get("/rates", response_class=HTMLResponse)
async def get_rates(request: Request):
    logging.info("Get Rates")
    countries = get_all_countries()
    context = {"request": request, "countries": []}
    is_visible = True
    for country in countries:
        rates = scripts.get_rates_from_db(f"rates.{country}", pg.PG_CLIENT)
        context["countries"].append(
            {
            "index": country,
            "name": COUNTRIES[country],
            "tech_rates": tech_rates(rates),
            "rates": round_rates(rates),
            "is_visible": "" if is_visible else "not-shown",
            "enabled_button": "disabled" if is_visible else ""
            }
        )
        is_visible=False
    logging.info(countries)
    return templates.TemplateResponse("final.html", context)

