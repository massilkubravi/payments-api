# Payments API

A backend payment processing system built using **FastAPI, PostgreSQL, and SQLAlchemy**.

## Features

- Create user accounts
- Check account balances
- Transfer money between accounts
- Prevent duplicate transactions using idempotency keys
- Refund completed transfers
- View transaction history
- Database transactions and row-level locking
- Automated API testing using Pytest

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

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd payments-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure PostgreSQL

Create a PostgreSQL database named `payments_db`.

Set your database connection string using the `DATABASE_URL` environment variable.

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## Running Tests

Configure `TEST_DATABASE_URL` to point to a separate PostgreSQL test database.

Run:

```bash
pytest -v
```

## Concepts Demonstrated

REST API development, relational database design, transaction management, idempotency, row-level locking, and automated testing.
