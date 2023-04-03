from http import HTTPStatus

from fastapi import FastAPI

from app.db.base import database

api = FastAPI()

not_found_response = {HTTPStatus.NOT_FOUND.value: {'model': None}}


@api.on_event('startup')
async def startup():
    await database.connect()


@api.on_event('shutdown')
async def shutdown():
    await database.disconnect()
