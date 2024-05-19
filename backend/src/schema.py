from pydantic import BaseModel

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

class FoodInfo(BaseModel):
    certainty: float | int
    food_name: str
    calories_Kcal: float | int
    fat_in_g: float | int
    protein_in_g: float | int
    sugar_in_g: float | int

    class Config:
        orm_mode = True
