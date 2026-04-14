from datetime import datetime
from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"