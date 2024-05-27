from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError
from .config import settings
import time
from .logger import setup_logger
from typing import Generator

logger = setup_logger(__name__)

# Function to create the database URL for PostgreSQL
def create_postgres_url():
    return URL.create(
        drivername="postgresql+psycopg2",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB
    )

def create_sqlite_engine():
    return create_engine("sqlite:///./test.db")

# Check if we are in development mode
is_development = settings.ENV == "development"

# Try to create an engine for PostgreSQL only if not in development
if not is_development:
    try:
        time.sleep(5) # give some time for DB to start
        db_url = create_postgres_url()
        engine = create_engine(db_url)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("--------Connected to PostgreSQL--------")
    except OperationalError as e:
        logger.error(f"PostgreSQL not available. Falling back to SQLite. Error: {e}")
        engine = create_sqlite_engine()
else:
    logger.info("Development mode detected. Using SQLite.")
    engine = create_sqlite_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
