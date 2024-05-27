from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .models import User
from .schemas import UserCreate

from .logger import setup_logger

logger = setup_logger(__name__)

def get_db_type(engine: Engine) -> str:
    if 'postgresql' in str(engine.url):
        logger.info("PostgreSQL")
        return "PostgreSQL"
    elif 'sqlite' in str(engine.url):
        logger.info("SQLite")
        return "SQLite"
    return "Unknown"

async def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

async def create_user(user: UserCreate, db: Session):
    user_obj = User(email=user.email, hashed_password=bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj
