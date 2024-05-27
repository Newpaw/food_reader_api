from pydantic import BaseModel, ConfigDict

class UserInfoRequest(BaseModel):
    user_id: int
    height_cm: float
    weight_kg: float
    age: float
    gender: str
    activity_level: str

class UserInfoRequestModel(UserInfoRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)

class FoodInfo(BaseModel):
    certainty: float | int
    food_name: str
    calories_Kcal: float | int
    fat_in_g: float | int
    protein_in_g: float | int
    sugar_in_g: float | int

    model_config = ConfigDict(from_attributes=True)
