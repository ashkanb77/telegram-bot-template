# db.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator, Annotated


from config import settings

engine = create_async_engine(
    settings.database_url,
    future=True,
    echo=False,
    # pool settings (tune to your workload)
    pool_size=10,
    max_overflow=20,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        return session

