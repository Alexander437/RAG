from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.settings import settings

DATABASE_URL = settings.get_url
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
