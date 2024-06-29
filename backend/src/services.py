import os
from jwt import encode, decode
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from fastapi import Depends, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import models as _models 
from . import schemas as _schemas
from .config import settings
from .logger import setup_logger
from .database import get_db
from .openai_client.client import OpenAIClient

logger = setup_logger(__name__)

oauth2schema = OAuth2PasswordBearer(tokenUrl="/token")

db_dependency = Annotated[Session, Depends(get_db)]

def get_db_type(engine: Engine) -> str:
    if 'postgresql' in str(engine.url):
        logger.info("PostgreSQL")
        return "PostgreSQL"
    elif 'sqlite' in str(engine.url):
        logger.info("SQLite")
        return "SQLite"
    return "Unknown"


async def get_user_by_email(email: str, db: Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: Session):
    user_obj = _models.User(email=user.email,
                    hashed_password=bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def get_user(user_id: int, db: Session):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(email, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def create_token(user: _models.User):
    user_obj = _schemas.User.model_validate(user)
    token = encode(user_obj.model_dump(), settings.JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: db_dependency, token: str = Depends(oauth2schema)):
    try:
        payload = decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        return HTTPException(status_code=401, detail="Invalid email or password")
    finally:
        return _schemas.User.model_validate(user)


async def get_user_metrics(user_id: int, db: db_dependency) -> _models.UserMetricsDB:
    return db.query(_models.UserMetricsDB).filter(_models.UserMetricsDB.owner_id == user_id).first()


async def get_user_calculated_daily_intake(user_id: int, db: db_dependency) -> _schemas.DailyIntakeBase:
    return db.query(_models.UserCalories).filter(_models.UserCalories.owner_id == user_id).first()


async def get_calculated_daily_intake(user_metrics=_schemas.UserMetrics) -> _schemas.DailyIntakeBase:
    if user_metrics.gender == "male":
        bmr = 88.362 + (13.397 * user_metrics.weight_kg) + \
            (4.799 * user_metrics.height_cm) - (5.677 * user_metrics.age)
    else:
        bmr = 447.593 + (9.247 * user_metrics.weight_kg) + \
            (3.098 * user_metrics.height_cm) - (4.330 * user_metrics.age)

    activity_factors = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.725
    }

    daily_calories = bmr * activity_factors[user_metrics.activity_level]

    protein_g = round(user_metrics.weight_kg * 1.2, 2)
    fat_g = round(daily_calories * 0.25 / 9, 2)
    user_metrics = round(daily_calories * 0.1 / 4, 2)
    sugar_g = round(daily_calories * 0.1 / 4, 2)
    return _schemas.DailyIntakeBase(calories=daily_calories, protein_g=protein_g, fat_g=fat_g, user_metrics=user_metrics, sugar_g=sugar_g)


async def save_daily_intake_to_db(owner_id: int, daily_intake: _schemas.DailyIntakeBase, db: db_dependency):
    pass


async def store_food_info_to_db(food_info: _schemas.FoodInfo, db: db_dependency):
    try:
        db_transaction = _models.FoodInfoDB(**food_info.model_dump())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to store food info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


async def analyze_image_and_save_to_db(file: UploadFile, db: db_dependency):
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
