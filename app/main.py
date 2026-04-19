from fastapi import FastAPI
from app.core.config import settings
from app.api import auth,health,transactions,ml,chat
from fastapi.security import HTTPBearer

security=HTTPBearer()  # Define the security scheme for authentication

app=FastAPI(title=settings.app_name,debug=settings.debug)

app.include_router(health.router)
app.include_router(auth.router,prefix="/auth")
app.include_router(transactions.router, prefix="/transactions")
app.include_router(ml.router)
app.include_router(chat.router)

