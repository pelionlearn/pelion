import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from db.base import Base
import db.models  # registers models with Base
import asyncio


DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@postgres:5432/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())

Session = async_sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)


async def get_db():
    async with Session() as session:
        yield session
