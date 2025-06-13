import os
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine

def get_engine():
    db_url = os.getenv("DATABASE_ENGINE")
    if not db_url:
        raise RuntimeError("DATABASE_ENGINE is not set!")
    pool_size = int(os.getenv("DATABASE_POOL_SIZE") or 10)
    return create_engine(db_url, pool_size=pool_size)

def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

def check_availability_db() -> bool:
    try:
        engine = get_engine()
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("DB unavailable:", e)
        return False