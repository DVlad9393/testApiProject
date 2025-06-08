import os

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine

engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def check_availability_db() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except:
        return False