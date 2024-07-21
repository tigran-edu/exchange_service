import logging
from fastapi import Depends, Body, Cookie, Response, Request, APIRouter
import backend.source.clients.pg as pg
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import backend.source.scripts as scripts


router = APIRouter()
templates = Jinja2Templates(directory="/frontend")


@router.get("/rates", response_class=HTMLResponse)
async def get_rates(request: Request):
    logging.info("Get Rates")
    rates_am = scripts.get_rates_from_db("rates.am", pg.PG_CLIENT)
    context = {"request": request, "rates_am": rates_am}
    return templates.TemplateResponse("front.html", context)
