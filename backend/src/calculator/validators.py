from .models import UserInfo


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
                raise InvalidInputException(f"Field '{field}' is missing.")
            if not isinstance(user_info[field], field_type):
                raise InvalidInputException(f"Field '{field}' is not of type {field_type}.")

        if user_info["gender"] not in ["male", "female"]:
            raise InvalidInputException("Gender must be 'male' or 'female'.")

        if user_info["activity_level"] not in ["low", "medium", "high"]:
            raise InvalidInputException("Activity level must be 'low', 'medium', or 'high'.")

        return UserInfo(**user_info)
