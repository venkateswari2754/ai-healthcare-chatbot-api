from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file if present

# Example: mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/healthcaresense
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./healthcare.db",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for FastAPI routes to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()