from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    owner_name: Mapped[str] = mapped_column(String(100))

    balance: Mapped[int] = mapped_column(BigInteger, default=0)

    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="balance_non_negative"
        ),
    )


class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(primary_key=True)

    idempotency_key: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    from_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id")
    )

    to_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id")
    )

    amount: Mapped[int] = mapped_column(BigInteger)

    status: Mapped[str] = mapped_column(
        String(20),
        default="completed"
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    