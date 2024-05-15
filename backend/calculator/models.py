from dataclasses import dataclass


@dataclass
class UserInfo:
    height_cm: float
    weight_kg: float
    age: int
    gender: str
    activity_level: str

@dataclass
class DailyIntake:
    calories: float
    fat_g: float
    sugar_g: float
    protein_g: float