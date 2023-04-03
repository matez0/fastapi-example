from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.db.base import database

api = FastAPI()

not_found_response = {HTTPStatus.NOT_FOUND.value: {'model': None}}


class NotFoundError(Exception):
    pass


@api.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return PlainTextResponse(None, status_code=404)


@api.on_event('startup')
async def startup():
    await database.connect()


@api.on_event('shutdown')
async def shutdown():
    await database.disconnect()
