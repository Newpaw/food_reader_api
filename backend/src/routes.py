import os
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .database import SessionLocal, engine
from .response_processor import ResponseProcessor
from .openai_client import OpenAIClient
from .models import FoodInfo, Base, ColoriesToDB, FoodInfoToDB
from .config import settings
from .logger import setup_logger
from calculator.processors import IntakeProcessor
from calculator.models import DailyIntake


router = APIRouter()
logger = setup_logger("routes")

assistant_id = settings.ASSISTANT_ID


class UserInfoRequest(BaseModel):
    user_id: int
    height_cm: float
    weight_kg: float
    age: float
    gender: str
    activity_level: str

class UserInfoRequestModel(UserInfoRequest):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

Base.metadata.create_all(bind=engine)





@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.post("/calculate-intake", response_model=DailyIntake)
async def calculate_intake(user_info: UserInfoRequest, db: db_dependency):
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
    client = OpenAIClient()

    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        thread = client.create_thread()
        file_id = client.upload_file(temp_file_path)
        client.create_message(thread.id, file_id)

        run = client.create_and_poll_run(thread.id, assistant_id)

        if run.status == 'completed':
            messages = client.list_messages(thread.id)
            content = messages.data[0].content[0].text.value
            logger.debug(content)

            food_info = ResponseProcessor.process_response(content)
            db_transactio = FoodInfoToDB(**food_info.to_dict())
            db.add(db_transactio)
            db.commit()
            db.refresh(db_transactio)
            return food_info
        else:
            logger.error("Processing failed")
            raise HTTPException(
                status_code=500, detail=f"Processing failed with info: {content}")
    except HTTPException as e:
        db.rollback()
        raise e
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Clean up the temporary file
        db.close()


def setup_routes(app: FastAPI) -> None:
    app.include_router(router)
