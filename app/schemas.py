from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    owner_name: str
    initial_balance: int = Field(default=0, ge=0)


class AccountResponse(BaseModel):
    id: int
    owner_name: str
    balance: int

    model_config = {"from_attributes": True}


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: int = Field(gt=0)


class TransferResponse(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: int
    status: str

    model_config = {"from_attributes": True}