from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from .config import settings
from .logger import setup_logger
from .calculator.schemas import DailyIntake
from .schemas import UserInfoRequest, FoodInfo, UserCreate, User
from .services import get_db_type, get_user_by_email, create_user, authenticate_user, create_token, get_current_user, calculate_daily_intake_and_save_to_db, analyze_image_and_save_to_db


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
async def create_new_user(user: UserCreate, db: db_dependency):
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


@router.get("/users/me", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    """
    Endpoint to get the current user.
    """
    return user


@router.post("/calculate-intake", response_model=DailyIntake)
async def calculate_intake(user_info: UserInfoRequest, db: db_dependency):
    """
    Endpoint to calculate daily intake based on user information.
    """
    daily_intake = await calculate_daily_intake_and_save_to_db(user_info, db)
    return daily_intake


@router.post("/analyze-image", response_model=FoodInfo)
async def analyze_image(db: Session = Depends(get_db), file: UploadFile = File(...)):
    """
    Endpoint to analyze an image and extract food information using OpenAI.
    """
    food_info = await analyze_image_and_save_to_db(file, db)
    return food_info


def setup_routes(app: FastAPI) -> None:
    """
    Function to setup routes in the FastAPI application.
    """
    app.include_router(router)
