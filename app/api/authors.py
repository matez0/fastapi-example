from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from .main import api, not_found_response

AuthorId = str


class AuthorIn(BaseModel):
    name: str


class AuthorOut(AuthorIn):
    id: AuthorId


@api.post('/authors', status_code=HTTPStatus.CREATED)
async def request_create_author(data: AuthorIn) -> AuthorOut:
    return AuthorOut(**data.dict(), id='babe1234')


@api.get('/authors')
async def request_retrieve_authors() -> List[AuthorOut]:
    return [AuthorOut(name='Sarah Connor', id='babe1234')]


@api.get('/authors/{id}', responses=not_found_response)
async def request_retrieve_author_by_id(id: str) -> AuthorOut:
    return AuthorOut(name='Sarah Connor', id=id)


@api.patch('/authors/{id}', responses=not_found_response)
async def request_update_author(id: str, data: AuthorIn) -> AuthorOut:
    return AuthorOut(**data.dict(), id=id)


@api.delete('/authors/{id}', status_code=HTTPStatus.NO_CONTENT, responses=not_found_response)
async def request_delete_author(id: str) -> None:
    pass
