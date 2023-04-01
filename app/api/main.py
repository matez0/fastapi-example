from http import HTTPStatus

from fastapi import FastAPI

api = FastAPI()

not_found_response = {HTTPStatus.NOT_FOUND.value: {'model': None}}
