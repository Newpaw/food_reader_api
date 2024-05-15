import os
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from .response_processor import ResponseProcessor
from .openai_client import OpenAIClient
from .models import FoodInfo, DailyIntake
from .config import settings
from .logger import setup_logger
from .processors import IntakeProcessor

router = APIRouter()
logger = setup_logger("routes")

assistant_id = settings.ASSISTANT_ID
correct_username = settings.API_USERNAME
correct_password = settings.API_PASSWORD

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.get("/ping")
async def ping():
    return {"message": "pong"}


class UserInfoRequest(BaseModel):
    height_cm: float
    weight_kg: float
    age: int
    gender: str
    activity_level: str

@router.post("/calculate-intake", response_model=DailyIntake)
async def calculate_intake(user_info: UserInfoRequest):
    try:
        daily_intake = IntakeProcessor.process(user_info.dict())
        return daily_intake
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze-image", response_model=FoodInfo)
async def analyze_image(file: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(authenticate)):
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
            return food_info
        else:
            logger.error("Processing failed")
            raise HTTPException(status_code=500, detail="Processing failed")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Clean up the temporary file

def setup_routes(app: FastAPI) -> None:
    app.include_router(router)
