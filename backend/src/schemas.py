from pydantic import BaseModel, ConfigDict
import datetime


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserInfoRequest(BaseModel):
    owner_id: int
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
