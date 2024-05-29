import os
from jwt import encode, decode
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from .models import User, UserCalories, FoodInfoDB
from .schemas import UserCreate, UserInfoRequest, FoodInfo, User as PydanticUser
from .config import settings
from .logger import setup_logger
from .database import get_db
from .calculator.processors import IntakeProcessor
from .openai_client.client import OpenAIClient

logger = setup_logger(__name__)

oauth2schema = OAuth2PasswordBearer(tokenUrl="/token")


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
    user_obj = User(email=user.email,
                    hashed_password=bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()


async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(email, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def create_token(user: User):
    user_obj = PydanticUser.model_validate(user)
    token = encode(user_obj.model_dump(), settings.JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload = decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = db.query(User).get(payload["id"])
    except:
        return HTTPException(status_code=401, detail="Invalid email or password")
    finally:
        return PydanticUser.model_validate(user)


async def process_daily_intake(user_info: UserInfoRequest):
    return IntakeProcessor.process(user_info.model_dump())


async def save_daily_intake_to_db(daily_intake, db: Session):
    try:
        db_transaction = UserCalories(**daily_intake.model_dump())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save daily intake to DB: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


async def calculate_daily_intake(user_info: UserInfoRequest, db: Session = Depends(get_db)):
    try:
        return await process_daily_intake(user_info)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def store_food_info_to_db(food_info: FoodInfo, db: Session = Depends(get_db)):
    try:
        db_transaction = FoodInfoDB(**food_info.model_dump())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store food info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


async def analyze_image_and_save_to_db(file: UploadFile, db: Session = Depends(get_db)):
    """
    Endpoint to analyze an image and extract food information using OpenAI.
    """
    client = OpenAIClient()
    temp_file_path = f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        return client.process_image(temp_file_path)

    except HTTPException as e:
        db.rollback()
        logger.error(f"HTTP exception: {e.detail}")
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Internal server error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
