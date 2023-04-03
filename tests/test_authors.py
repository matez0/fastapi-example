from http import HTTPStatus
from unittest.mock import ANY

from fastapi.testclient import TestClient
import pytest

from app.api import api
from app.db.base import engine, metadata


@pytest.fixture
def client(tmp_path):
    empty_db()
    return TestClient(api)


def empty_db():
    with engine.connect() as connection, connection.begin():
        for table in reversed(metadata.sorted_tables):
            connection.execute(table.delete())


@pytest.fixture
def create_author(client):
    def _create_author(author):
        return client.post('/authors', json=author).json()

    return _create_author


def test_create_author(client):
    author = {'name': 'Sarah Connor'}

    response = client.post('/authors', json=author)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == dict(author, id=ANY)


def test_retrieve_authors(client, create_author):
    response = client.get('/authors')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

    authors = [
        create_author({'name': 'Sarah Connor'}),
        create_author({'name': 'Kyle Reese'}),
    ]

    response = client.get('/authors')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == authors


def test_retrieve_author_by_id(client, create_author):
    author = create_author({'name': 'John Connor'})

    response = client.get(f'/authors/{author["id"]}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == author


def test_update_author(client, create_author):
    author_id = create_author({'name': 'Sarah Connor'})['id']
    updated_author = {'name': 'Miles Dyson'}

    response = client.patch(f'/authors/{author_id}', json=updated_author)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == dict(updated_author, id=author_id)


def test_delete_author(client, create_author):
    author_id = create_author({'name': 'Sarah Connor'})['id']

    response = client.delete(f'/authors/{author_id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert client.get(f'/authors/{author_id}').status_code == HTTPStatus.NOT_FOUND


def test_respond_not_found_when_updating_non_existing_author(client):
    response = client.patch('/authors/1', json={'name': 'Miles Dyson'})

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_respond_not_found_when_deleting_non_existing_author(client):
    response = client.delete('/authors/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
