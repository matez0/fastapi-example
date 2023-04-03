from http import HTTPStatus
from typing import List

from pydantic import BaseModel

from app.db.base import CrudMixin
from app.db.tables import Book
from .authors import AuthorId
from .main import api, NotFoundError, not_found_response


class BookIn(BaseModel):
    name: str
    author_id: AuthorId


class BookOut(BookIn, CrudMixin):
    id: str

    obj = Book

    class Config:
        orm_mode = True


@api.post('/books', status_code=HTTPStatus.CREATED)
async def request_create_book(data: BookIn) -> BookOut:
    return await BookOut.create(**data.dict())


@api.get('/books')
async def request_retrieve_books(authorId: AuthorId = None) -> List[BookOut]:
    conditions = {} if authorId is None else dict(author_id=authorId)
    return await BookOut.get(**conditions)


@api.get('/books/{id}', responses=not_found_response)
async def request_retrieve_book_by_id(id: str) -> BookOut:
    books = await BookOut.get(id=id)

    if not books:
        raise NotFoundError

    return books[0]


@api.patch('/books/{id}', responses=not_found_response)
async def request_update_book(id: str, data: BookIn) -> BookOut:
    book = await BookOut.update(id, **data.dict())

    if not book:
        raise NotFoundError

    return book


@api.delete('/books/{id}', status_code=HTTPStatus.NO_CONTENT, responses=not_found_response)
async def request_delete_book(id: str) -> None:
    if not await BookOut.delete(id):
        raise NotFoundError
