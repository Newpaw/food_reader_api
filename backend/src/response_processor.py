import json
import re
from fastapi import HTTPException
from .schema import FoodInfo
from .logger import setup_logger

logger = setup_logger("response_processor")

class InvalidFormatException(Exception):
    pass

class ResponseValidator:
    @staticmethod
    def validate_and_convert(json_data):
        required_fields = {
            "food_name": str,
            "calories_Kcal": (int, float),
            "certainty": (int, float),
            "fat_in_g": (int, float),
            "protein_in_g": (int, float),
            "sugar_in_g": (int, float),
        }

        # Validate required fields
        for field, field_type in required_fields.items():
            if field not in json_data:
                raise InvalidFormatException(f"Field '{field}' is missing.")
            if not isinstance(json_data[field], field_type):
                try:
                    if field_type == (int, float):
                        json_data[field] = float(json_data[field])
                except ValueError:
                    raise InvalidFormatException(
                        f"Field '{field}' is not of type {field_type}.")

        return json_data

class ResponseProcessor:
    @staticmethod
    def process_response(content: str) -> FoodInfo:
        # Extract JSON content using regular expression
        match = re.search(r'({.*?})', content, re.DOTALL)
        if match:
            clean_content = match.group(1).strip()
        else:
            logger.error(f"JSON decode error: Invalid JSON format. The response was: {content}")
            raise HTTPException(
                status_code=422, detail=f"Invalid JSON format. The response was: {content}")

        try:
            json_data = json.loads(clean_content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}. The response was: {content}")
            raise HTTPException(
                status_code=422, detail=f"Invalid JSON format. The response was: {content}")

        try:
            json_data = ResponseValidator.validate_and_convert(json_data)
        except InvalidFormatException as e:
            logger.error(f"Validation error: {e}")
            raise HTTPException(
                status_code=422, detail=f"{str(e)}. The response was: {content}")

        try:
            food_info = FoodInfo(
                certainty=json_data["certainty"],
                food_name=json_data["food_name"],
                calories_Kcal=json_data["calories_Kcal"],
                fat_in_g=json_data["fat_in_g"],
                protein_in_g=json_data["protein_in_g"],
                sugar_in_g=json_data["sugar_in_g"],
            )
        except KeyError as e:
            logger.error(f"Key error: {e}")
            raise HTTPException(
                status_code=422, detail=f"Missing field: {str(e)}")
        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise HTTPException(
                status_code=422, detail=f"Invalid value: {str(e)}")

        return food_info
