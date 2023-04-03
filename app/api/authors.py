from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from app.db.base import CrudMixin
from app.db.tables import Author
from .main import api, NotFoundError, not_found_response

AuthorId = str


class AuthorIn(BaseModel):
    name: str


class AuthorOut(AuthorIn, CrudMixin):
    id: AuthorId

    obj = Author

    class Config:
        orm_mode = True


@api.post('/authors', status_code=HTTPStatus.CREATED)
async def request_create_author(data: AuthorIn) -> AuthorOut:
    return await AuthorOut.create(**data.dict())


@api.get('/authors')
async def request_retrieve_authors() -> List[AuthorOut]:
    return await AuthorOut.get()


@api.get('/authors/{id}', responses=not_found_response)
async def request_retrieve_author_by_id(id: str) -> AuthorOut:
    authors = await AuthorOut.get(id=id)

    if not authors:
        raise NotFoundError

    return authors[0]


@api.patch('/authors/{id}', responses=not_found_response)
async def request_update_author(id: str, data: AuthorIn) -> AuthorOut:
    author = await AuthorOut.update(id, **data.dict())

    if not author:
        raise NotFoundError

    return author


@api.delete('/authors/{id}', status_code=HTTPStatus.NO_CONTENT, responses=not_found_response)
async def request_delete_author(id: str) -> None:
    if not await AuthorOut.delete(id):
        raise NotFoundError
