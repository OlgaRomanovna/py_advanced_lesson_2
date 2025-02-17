import logging
import os
import dotenv
import pytest
from sqlalchemy import delete

from app.models.User import User

dotenv.load_dotenv()

from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import create_engine, SQLModel, text

engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))


def create_db_and_tables():
    logging.info("Creating tables...")
    SQLModel.metadata.create_all(engine)
    logging.info("Tables created.")


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False
