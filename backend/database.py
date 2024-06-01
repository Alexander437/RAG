from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from backend.settings import settings

DATABASE_URL = settings.USER_DB_CONFIG.get_url
Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# alembic init migrations
# configure migrations/env.py
# alembic revision --autogenerate -m "Database creation"
# alembic upgrade dbd902a137b0
# alembic upgrade head
# insert into role values (1, 'user', null);
