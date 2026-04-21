import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.auth import get_current_user
from rag.graph import run_chat

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id)
    )
    transactions = result.scalars().all()
    transaction_data = [{"amount": float(t.amount), "category": t.category} for t in transactions]

    try:
        response = await asyncio.to_thread(run_chat, request.query, transaction_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
    return {"query": request.query, "response": response}
