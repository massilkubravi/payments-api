
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import Base, engine, get_db
from .models import Account, Transfer
from .schemas import (
    AccountCreate,
    AccountResponse,
    TransferCreate,
    TransferResponse
)
from .services import create_transfer, refund_transfer


app = FastAPI(title="Payments API")


# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Payments API is running successfully!"}


# Create a new account
@app.post("/accounts", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db)
):
    new_account = Account(
        owner_name=account.owner_name,
        balance=account.initial_balance
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


# Check account balance
@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = db.get(Account, account_id)

    if not account:
        raise HTTPException(404, "Account not found")

    return account


# Transfer money
@app.post("/transfers", response_model=TransferResponse)
def transfer_money(
    transfer: TransferCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: Session = Depends(get_db)
):
    result = create_transfer(
        db,
        transfer,
        idempotency_key
    )

    return result


# View a transfer
@app.get("/transfers/{transfer_id}", response_model=TransferResponse)
def get_transfer(
    transfer_id: int,
    db: Session = Depends(get_db)
):
    transfer = db.get(Transfer, transfer_id)

    if not transfer:
        raise HTTPException(404, "Transfer not found")

    return transfer


# View transaction history
@app.get("/accounts/{account_id}/transfers")
def transaction_history(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = db.get(Account, account_id)

    if not account:
        raise HTTPException(404, "Account not found")

    transfers = db.scalars(
        select(Transfer).where(
            (Transfer.from_account_id == account_id) |
            (Transfer.to_account_id == account_id)
        )
    ).all()

    return transfers


# Refund a transfer
@app.post(
    "/transfers/{transfer_id}/refund",
    response_model=TransferResponse
)
def refund_money(
    transfer_id: int,
    db: Session = Depends(get_db)
):
    return refund_transfer(db, transfer_id)
