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