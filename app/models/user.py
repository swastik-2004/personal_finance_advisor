from sqlalchemy import Column,Integer,String,DateTime,Boolean
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    password_hash=Column(String,nullable=False)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.utcnow)