from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from .database import get_db
from .config import settings
from .logger import setup_logger
from .models import UserMetricsDB, UserCalories
from . import schemas as _schemas
from . import exceptions as _exceptions
from .services import (
    get_db_type,
    get_user_by_email,
    create_user,
    authenticate_user,
    create_token,
    get_current_user,
    analyze_image_and_save_to_db,
    store_food_info_to_db,
    get_calculated_daily_intake,
    get_user_metrics,
    get_user_calculated_daily_intake,
)

router = APIRouter()
logger = setup_logger(__name__)

assistant_id = settings.ASSISTANT_ID
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
async def root(db: db_dependency):
    """
    Root endpoint to check if the database is running.
    """
    try:
        result = db.execute(text("SELECT 1")).scalar()
        db_type = get_db_type(db.get_bind())
        if result == 1:
            return {"status": "success", "message": "Database is running.", "database_type": db_type}
        else:
            return {"status": "error", "message": "Unexpected result from database.", "database_type": db_type}
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return {"status": "error", "message": "Database is not running.", "database_type": "Unknown"}


@router.get("/ping")
async def ping():
    """
    Simple endpoint for health check.
    """
    return {"message": "pong"}


@router.post("/users")
async def create_new_user(user: _schemas.UserCreate, db: db_dependency):
    """
    Endpoint to create a new user.
    """
    logger.debug(f"Creating user with email: {user.email}")
    db_user = await get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    created_user = await create_user(user, db)
    return await create_token(created_user)


@router.post("/token")
async def generate_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to generate a token for a user.
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return await create_token(user)


@router.get("/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = Depends(get_current_user)):
    """
    Endpoint to get the current user.
    """
    return user


@router.post("/calculate-intake", response_model=_schemas.DailyIntakeBase)
async def calculate_intake(user_metrics: _schemas.UserMetrics, db: db_dependency, user: _schemas.User = Depends(get_current_user)):
    """
    Endpoint to calculate daily intake based on user information.
    """
    user_daily_intake = await get_calculated_daily_intake(user_metrics)

    user_met_obj = UserMetricsDB(owner_id=user.id, height_cm=user_metrics.height_cm, weight_kg=user_metrics.weight_kg,
                                 age=user_metrics.age, gender=user_metrics.gender, activity_level=user_metrics.activity_level)
    try:
        db.add(user_met_obj)
        db.commit()
        db.refresh(user_met_obj)
    except IntegrityError:
        db.rollback()
        raise _exceptions.UniqueConstraintFailedException(detail="User metrics already exist for this user.")

    user_cal_obj = UserCalories(owner_id=user.id, calories=user_daily_intake.calories, fat_g=user_daily_intake.fat_g,
                                sugar_g=user_daily_intake.sugar_g, protein_g=user_daily_intake.protein_g)
    db.add(user_cal_obj)
    db.commit()
    db.refresh(user_cal_obj)

    return user_daily_intake.model_dump()

@router.get("/users/me/metrics", response_model=_schemas.UserMetrics)
async def user_metrics(db: db_dependency, user: _schemas.User = Depends(get_current_user)):
    """
    Endpoint to get user metrics.
    """
    user_metrics = await get_user_metrics(user.id, db)
    if user_metrics is None:
        raise HTTPException(status_code=404, detail="User metrics not found")
    return user_metrics



@router.get("/users/me/daily-intake", response_model=_schemas.DailyIntakeBase)
async def daily_intake(db: db_dependency, user: _schemas.User = Depends(get_current_user)):
    """
    Endpoint to get user daily intake.
    """
    user_daily_intake = await get_user_calculated_daily_intake(user.id, db)
    if user_daily_intake is None:
        raise HTTPException(status_code=404, detail="User daily intake not found")
    return user_daily_intake




@router.post("/analyze-image", response_model=_schemas.FoodInfo)
async def analyze_image(db: Session = Depends(get_db), file: UploadFile = File(...)):
    """
    Endpoint to analyze an image and extract food information using OpenAI.
    """
    food_info = await analyze_image_and_save_to_db(file, db)
    await store_food_info_to_db(food_info, db)
    return food_info


def setup_routes(app: FastAPI) -> None:
    """
    Function to setup routes in the FastAPI application.
    """
    app.include_router(router)
