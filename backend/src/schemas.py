from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int

    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class DailyIntakeBase(BaseModel):
    calories: float
    fat_g: float
    sugar_g: float
    protein_g: float

    model_config = ConfigDict(orm_mode=True, from_attributes=True)



class DailyIntakeCreate(DailyIntakeBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)



class UserMetrics(BaseModel):
    height_cm: float
    weight_kg: float
    age: float
    gender: str
    activity_level: str

    model_config = ConfigDict(orm_mode=True, from_attributes=True)


class FoodInfo(BaseModel):
    certainty: float | int
    food_name: str
    calories_Kcal: float | int
    fat_in_g: float | int
    protein_in_g: float | int
    sugar_in_g: float | int

    model_config = ConfigDict(from_attributes=True)
