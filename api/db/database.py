import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.db.base import Base
import api.db.models  # registers models with Base


DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@postgres:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autoflush=True)
