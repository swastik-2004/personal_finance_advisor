from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_validator

class TransactionCreate(BaseModel):
    amount: float
    description: str
    category: str | None
    transaction_type: str
    date: datetime

    @field_validator("date")
    @classmethod
    def strip_timezone(cls, v: datetime) -> datetime:
        return v.astimezone(timezone.utc).replace(tzinfo=None)

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: datetime
    category: str | None
    transaction_type: str
    model_config = ConfigDict(from_attributes=True)