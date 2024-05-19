import os
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from .database import get_db
from .response_processor import ResponseProcessor
from .openai_client.client import OpenAIClient
from .models import ColoriesToDB, FoodInfoToDB
from .config import settings
from .logger import setup_logger
from .calculator.processors import IntakeProcessor
from .calculator.models import DailyIntake
from .schema import UserInfoRequest, FoodInfo

router = APIRouter()
logger = setup_logger("routes")

assistant_id = settings.ASSISTANT_ID
db_dependency = Annotated[Session, Depends(get_db)]


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
        db_transaction = ColoriesToDB(**daily_intake.to_dict())
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
        # Uložení souboru dočasně na disk
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Interakce s OpenAI klientem
        thread = client.create_thread()
        file_id = client.upload_file(temp_file_path)
        client.create_message(thread.id, file_id)

        run = client.create_and_poll_run(thread.id, assistant_id)

        if run.status == "completed":
            messages = client.list_messages(thread.id)
            content = messages.data[0].content[0].text.value
            logger.debug(content)

            # Zpracování odpovědi a uložení do databáze
            food_info = ResponseProcessor.process_response(content)
            db_transaction = FoodInfoToDB(**food_info.model_dump())
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return food_info
        else:
            logger.error("Processing failed")
            raise HTTPException(
                status_code=500, detail=f"Processing failed with info: {content}"
            )
    except HTTPException as e:
        db.rollback()
        raise e
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Čištění dočasného souboru
        db.close()


def setup_routes(app: FastAPI) -> None:
    """
    Function to setup routes in the FastAPI application.
    """
    app.include_router(router)
