from dataclasses import dataclass

@dataclass
class FoodComposition:
    fat_in_g: float | int
    protein_in_g: float | int
    sugar_in_g: float | int

@dataclass
class FoodInfo:
    certainty: float | int
    food_name: str
    calories_Kcal: float | int
    food_composition: FoodComposition


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