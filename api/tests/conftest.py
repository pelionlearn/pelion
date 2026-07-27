import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from db.base import Base
from db.database import engine, get_db


@pytest.fixture
async def db_session():
    # use the engine and connection from db.database
    async with engine.connect() as connection:
        # start a transaction for this test so we can rollback later
        transaction = await connection.begin()

        # new session bound to the db.database engine connection
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        yield session

        await session.close()
        await transaction.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test", follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()
