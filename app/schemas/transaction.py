from datetime import datetime
from pydantic import BaseModel,ConfigDict

class TransactionCreate(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    category: str | None
    transaction_type: str
    date: datetime

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: datetime
    category: str | None
    transaction_type: str
    model_config = ConfigDict(from_attributes=True)