import os
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text


from .database import get_db
from .response_processor import ResponseProcessor
from .openai_client.client import OpenAIClient
from .models import UserCalories, FoodInfoDB
from .config import settings
from .logger import setup_logger
from .calculator.processors import IntakeProcessor
from .calculator.models import DailyIntake
from .schemas import UserInfoRequest, FoodInfo, UserCreate
from .services import get_db_type, get_user_by_email, create_user

router = APIRouter()
logger = setup_logger(__name__)

assistant_id = settings.ASSISTANT_ID
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/users")
async def create_new_user(user: UserCreate, db: db_dependency):
    """
    Endpoint to create a new user.
    """
    db_user = await get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return await create_user(user, db) 

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


@router.post("/calculate-intake", response_model=DailyIntake)
async def calculate_intake(user_info: UserInfoRequest, db: db_dependency):
    """
    Endpoint to calculate daily intake based on user information.
    """
    try:
        daily_intake = IntakeProcessor.process(user_info.model_dump())
        db_transaction = UserCalories(**daily_intake.to_dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return daily_intake
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


@router.post("/analyze-image", response_model=FoodInfo)
async def analyze_image(db: db_dependency, file: UploadFile = File(...)):
    """
    Endpoint to analyze an image and extract food information using OpenAI.
    """
    client = OpenAIClient()

    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        thread = client.create_thread()
        logger.debug(f"Created thread with thread_id: {thread.id}")

        file_id = client.upload_file(temp_file_path)
        logger.debug(f"Uploaded file with file_id: {file_id}")

        client.create_message(thread.id, file_id)

        run = client.create_and_poll_run(thread.id, assistant_id)
        logger.debug(f"Created and polled run with run_id: {run.id}")

        if run.status == "completed":
            messages = client.list_messages(thread.id)
            content = messages.data[0].content[0].text.value
            logger.debug(f"Content: {content}")

            # Zpracování odpovědi a uložení do databáze
            food_info = ResponseProcessor.process_response(content)
            db_transaction = FoodInfoDB(**food_info.model_dump())
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return food_info
        else:
            logger.error("Processing failed")
            raise HTTPException(
                status_code=500, detail="Processing failed with no additional info"
            )
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Čištění dočasného souboru
        db.close()


def setup_routes(app: FastAPI) -> None:
    """
    Function to setup routes in the FastAPI application.
    """
    app.include_router(router)
