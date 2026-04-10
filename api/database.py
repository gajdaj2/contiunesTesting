# database.py – konfiguracja połączenia z bazą

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# produkcyjna baza (SQLite dla uproszczenia)
DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base jest importowany przez models.py i conftest.py
Base = declarative_base()