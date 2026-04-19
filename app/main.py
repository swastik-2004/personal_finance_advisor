from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth,health,transactions,ml,chat
from fastapi.security import HTTPBearer

security=HTTPBearer()

app=FastAPI(title=settings.app_name,debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router,prefix="/auth")
app.include_router(transactions.router, prefix="/transactions")
app.include_router(ml.router)
app.include_router(chat.router)

