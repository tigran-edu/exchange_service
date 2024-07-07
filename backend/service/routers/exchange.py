from fastapi import Depends, Body, Cookie, Response, status, APIRouter
from backend.source.clients.pg import PG_CLIENT
# import logging
import backend.source.scripts as scripts
from backend.source.clients.parser import Parser, CONFIG


router = APIRouter()


@router.get("/rates")
async def get_rates(response: Response):
    return await Parser.pars(CONFIG["ARMENIA"])
