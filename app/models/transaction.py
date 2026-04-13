from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,Numeric
from datetime import datetime
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    amount=Column(Numeric(10,2),nullable=False)
    description=Column(String,nullable=True)
    category=Column(String,nullable=True)
    transaction_type=Column(String,nullable=False)  # e.g., "income" or "expense"
    date=Column(DateTime,default=datetime.utcnow)
    