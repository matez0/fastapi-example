from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from .authors import AuthorId
from .main import api, not_found_response


class BookIn(BaseModel):
    name: str
    author_id: AuthorId


class BookOut(BookIn):
    id: str


@api.post('/books', status_code=HTTPStatus.CREATED)
async def request_create_book(data: BookIn) -> BookOut:
    return BookOut(**data.dict(), id='1dae9999')


@api.get('/books')
async def request_retrieve_books(authorId: AuthorId = None) -> List[BookOut]:
    return [BookOut(name='Terminator', id='1dae9999')]


@api.get('/books/{id}', responses=not_found_response)
async def request_retrieve_book_by_id(id: str) -> BookOut:
    return BookOut(name='Terminator', id=id)


@api.patch('/books/{id}', responses=not_found_response)
async def request_update_book(id: str, data: BookIn) -> BookOut:
    return BookOut(**data.dict(), id=id)


@api.delete('/books/{id}', status_code=HTTPStatus.NO_CONTENT, responses=not_found_response)
async def request_delete_book(id: str) -> None:
    pass
