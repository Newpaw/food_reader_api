from .models import UserInfo
from ..logger import setup_logger

logger = setup_logger(__name__)


class InvalidInputException(Exception):
    pass

class InputValidator:
    @staticmethod
    def validate(user_info: dict) -> UserInfo:
        required_fields = {
            "height_cm": float,
            "weight_kg": float,
            "age": float,
            "gender": str,
            "activity_level": str
        }

        for field, field_type in required_fields.items():
            if field not in user_info:
                logger.error(f"Field '{field}' is missing.")
                raise InvalidInputException(f"Field '{field}' is missing.")
            if not isinstance(user_info[field], field_type):
                logger.error(f"Field '{field}' is not of type {field_type}.")
                raise InvalidInputException(f"Field '{field}' is not of type {field_type}.")

        if user_info["gender"] not in ["male", "female"]:
            logger.error("Gender must be 'male' or 'female'.")
            raise InvalidInputException("Gender must be 'male' or 'female'.")

        if user_info["activity_level"] not in ["low", "medium", "high"]:
            logger.error("Activity level must be 'low', 'medium', or 'high'.")
            raise InvalidInputException("Activity level must be 'low', 'medium', or 'high'.")
        logger.info("Input is valid.")
        return UserInfo(**user_info)
