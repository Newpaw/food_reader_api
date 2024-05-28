from pydantic import BaseModel, Field, ConfigDict

class UserInfo(BaseModel):
    owner_id: int
    height_cm: float
    weight_kg: float
    age: float
    gender: str
    activity_level: str

    model_config = ConfigDict(orm_mode=True, from_attributes=True)

class DailyIntake(BaseModel):
    owner_id: int
    calories: float
    fat_g: float
    sugar_g: float
    protein_g: float

    model_config = ConfigDict(orm_mode=True, from_attributes=True)
