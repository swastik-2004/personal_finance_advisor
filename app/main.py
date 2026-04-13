from fastapi import FastAPI
from app.core.config import settings
from app.api import auth,health

app=FastAPI(title=settings.app_name,debug=settings.debug)

app.include_router(health.router)
app.include_router(auth.router,prefix="/auth")