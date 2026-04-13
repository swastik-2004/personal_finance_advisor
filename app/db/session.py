from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings



async_session_factory = sessionmaker(
    create_async_engine(settings.database_url, echo=True),
    class_=AsyncSession,
    expire_on_commit=False)

async def get_db():
    async with async_session_factory() as session:
        yield session