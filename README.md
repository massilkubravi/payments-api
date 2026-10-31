# Payments API

A backend payment processing API built using **FastAPI, PostgreSQL, and SQLAlchemy**.

## Features

- Create and manage user accounts
- Check account balances
- Transfer money between accounts
- Prevent duplicate transactions using idempotency keys
- Refund completed transfers
- View transaction history
- Database transactions and row-level locking
- Automated API tests using Pytest

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- HTTPX

## Project Structure

```text
payments-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── test/
│   ├── conftest.py
│   └── test_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Running Locally

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database named `payments_db`.
5. Configure the `DATABASE_URL` environment variable with your database credentials.
6. Start the API:

```bash
uvicorn app.main:app --reload
```

7. Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Configure `TEST_DATABASE_URL` to point to a separate PostgreSQL test database, then run:

```bash
pytest -v
```

## Key Concepts Demonstrated

REST API development, relational database design, transaction management, idempotency, database locking, and automated testing.
