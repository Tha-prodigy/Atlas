import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.config import settings
from app.database.base import Base
from app.models import Country, Category, Business, BusinessModel, Opportunity


@pytest_asyncio.fixture
async def db_session():

    engine = create_async_engine(
        settings.test_database_url,
        echo=False
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    try:
        async with SessionLocal() as session:
            yield session

    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await engine.dispose()