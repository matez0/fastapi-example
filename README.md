# Authors and books

This is an example for implementing a REST API using FastAPI and coroutines and the following features:
- request body validation
- response body validation
- query parameter
- non default response code
- indicating additional response schemas with different response status
- exception handling

The REST API provides CRUD operations for author and book models where each book has one author.

`Author(id, name)`:
- create: POST /authors
- retrieve:
  - GET /authors
  - GET /authors/{id}
- update: PATCH /authors/{id}
- delete: DELETE /authors/{id}

`Book(id, name, author_id)`:
- create: POST /books
- retrieve:
  - GET /books with optional filter by author ID
  - GET /books/{id}
- update: PATCH /books/{id}
- delete: DELETE /books/{id}

Data are stored using `sqlite`.

## Testing

Go to the directory of the git repository.

Create and activate a Python virtual environment:
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```
Install dependencies:
```
pip install -r requirements.txt
```
Run end-to-end tests:
```
pytest -v
```

## Running the application

Go to the directory of the git repository and activate the virtual environment.

Start the application:
```
uvicorn app.api:api
```
Check the generated OpenApi documentation:
```
${BROWSER} http://localhost:8000/docs
```
Perform a request to an endpoint, e.g.:
```
curl -i -X POST http://localhost:8000/authors -H 'content-type: application/json' -d '{"name": "Kate Brewster"}'
```
