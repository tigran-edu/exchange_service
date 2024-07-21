from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.service.api.routers import exchange
from backend.source.clients.pg import create_pg_client, close_client
import uvicorn
import logging
import os


def get_uvicorn_config():
    uv_port = int(os.environ.get("UVICORN_PORT"))
    uv_host = os.environ.get("UVICORN_HOST")
    return uvicorn.Config("__init__:app", port=uv_port, host=uv_host)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Creating PG client")
    create_pg_client()
    yield
    close_client()


app = FastAPI(lifespan=lifespan)
app.include_router(exchange.router)


origins = [
    "http://localhost:3001",  # local debug
    "http://localhost:63342",  # local debug (Pycharm)
    "https://hse-am2.y.rnd-42.ru",  # server frontend address
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["*"],
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = uvicorn.Server(get_uvicorn_config())
    server.run()
