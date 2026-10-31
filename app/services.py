
from fastapi import HTTPException
from sqlalchemy import select

from .models import Account, Transfer


# CREATE MONEY TRANSFER
def create_transfer(db, data, idempotency_key):

    try:
        # 1. Check idempotency key
        print("Received key:", idempotency_key)

        existing = db.execute(
            select(Transfer)
            .where(Transfer.idempotency_key == idempotency_key)
        ).scalar_one_or_none()

        print("Existing transfer:", existing)

        # If request already exists, return previous transfer
        if existing:
            return existing

        # 2. Prevent transfer to same account
        if data.from_account_id == data.to_account_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot transfer to the same account"
            )

        # 3. Lock both accounts
        accounts = db.scalars(
            select(Account)
            .where(
                Account.id.in_([
                    data.from_account_id,
                    data.to_account_id
                ])
            )
            .order_by(Account.id)
            .with_for_update()
        ).all()

        by_id = {account.id: account for account in accounts}

        sender = by_id.get(data.from_account_id)
        receiver = by_id.get(data.to_account_id)

        # 4. Check accounts exist
        if not sender or not receiver:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        # 5. Check sufficient balance
        if sender.balance < data.amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance"
            )

        # 6. Transfer money
        sender.balance -= data.amount
        receiver.balance += data.amount

        # 7. Save transfer record
        transfer = Transfer(
            idempotency_key=idempotency_key,
            from_account_id=sender.id,
            to_account_id=receiver.id,
            amount=data.amount,
            status="completed"
        )

        db.add(transfer)
        db.commit()
        db.refresh(transfer)

        return transfer

    except Exception:
        db.rollback()
        raise


# REFUND MONEY TRANSFER
def refund_transfer(db, transfer_id):

    try:
        # 1. Find and lock original transfer
        transfer = db.execute(
            select(Transfer)
            .where(Transfer.id == transfer_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not transfer:
            raise HTTPException(
                status_code=404,
                detail="Transfer not found"
            )

        # 2. Check transfer status
        if transfer.status != "completed":
            raise HTTPException(
                status_code=400,
                detail="Transfer cannot be refunded"
            )

        # 3. Lock both accounts
        accounts = db.scalars(
            select(Account)
            .where(
                Account.id.in_([
                    transfer.from_account_id,
                    transfer.to_account_id
                ])
            )
            .order_by(Account.id)
            .with_for_update()
        ).all()

        by_id = {account.id: account for account in accounts}

        sender = by_id.get(transfer.from_account_id)
        receiver = by_id.get(transfer.to_account_id)

        if not sender or not receiver:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        # 4. Check receiver balance
        if receiver.balance < transfer.amount:
            raise HTTPException(
                status_code=409,
                detail="Insufficient balance for refund"
            )

        # 5. Return money to original sender
        receiver.balance -= transfer.amount
        sender.balance += transfer.amount

        # 6. Update transfer status
        transfer.status = "refunded"

        db.commit()
        db.refresh(transfer)

        return transfer

    except Exception:
        db.rollback()
        raise
