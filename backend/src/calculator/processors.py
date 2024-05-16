from ..core.logger import setup_logger
from fastapi import HTTPException
from .models import DailyIntake
from .validators import InputValidator, InvalidInputException
from .calculators import IntakeCalculator

logger = setup_logger("processors")

class IntakeProcessor:
    @staticmethod
    def process(user_info: dict) -> DailyIntake:
        try:
            validated_user_info = InputValidator.validate(user_info)
        except InvalidInputException as e:
            logger.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=str(e))
        
        daily_intake = IntakeCalculator.calculate_daily_intake(validated_user_info)
        return daily_intake
