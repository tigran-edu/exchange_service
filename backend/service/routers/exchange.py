from fastapi import Depends, Body, Cookie, Response, Request, APIRouter
import backend.source.clients.pg as pg
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import logging
import backend.source.scripts as scripts
from backend.source.clients.parser import Parser, CONFIG
from backend.source.parsers.basic import StatusCode


router = APIRouter()
templates = Jinja2Templates(directory="/frontend")


@router.get("/rates", response_class=HTMLResponse)
async def get_rates(request: Request):
    rates_am = scripts.get_rates_from_db("rates.am", pg.PG_CLIENT)
    context = {"request": request, "rates_am": rates_am}
    return templates.TemplateResponse("front.html", context)


@router.put("/rates")
async def update_rates(request: Request):
    scripts.create_rates_schema("rates", pg.PG_CLIENT)
    scripts.create_rates_table("rates.am", pg.PG_CLIENT)
    responses = await Parser.pars(CONFIG["ARMENIA"])
    responses = [resp for resp in responses if resp.return_code == StatusCode.OK]
    scripts.write_rates_to_db("rates.am", responses, pg.PG_CLIENT)
