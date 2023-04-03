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
def author_id():
    return 'feed5678'


def test_create_author(client):
    author = {'name': 'Sarah Connor'}

    response = client.post('/authors', json=author)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == dict(author, id=ANY)


def test_retrieve_authors(client):
    response = client.get('/authors')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [{'name': 'Sarah Connor', 'id': ANY}]


def test_retrieve_author_by_id(client, author_id):
    response = client.get(f'/authors/{author_id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': 'Sarah Connor', 'id': author_id}


def test_update_author(client, author_id):
    updated_author = {'name': 'Miles Dyson'}
    response = client.patch(f'/authors/{author_id}', json=updated_author)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == dict(updated_author, id=author_id)


def test_delete_author(client, author_id):
    response = client.delete(f'/authors/{author_id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    # FIXME: check that author cannot be retrieved anymore.


# FIXME: test when referred item does not exist.
