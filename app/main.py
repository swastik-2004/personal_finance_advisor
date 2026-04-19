from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.api import auth,health,transactions,ml,chat
from app.db.base import Base
import app.models.user
import app.models.transaction
import app.models.expense_category
from fastapi.security import HTTPBearer

security=HTTPBearer()

app=FastAPI(title=settings.app_name,debug=settings.debug)

@app.on_event("startup")
async def create_tables():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router,prefix="/auth")
app.include_router(transactions.router, prefix="/transactions")
app.include_router(ml.router)
app.include_router(chat.router)

