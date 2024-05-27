from dataclasses import dataclass, asdict


@dataclass
class UserInfo:
    owner_id: int
    height_cm: float
    weight_kg: float
    age: float
    gender: str
    activity_level: str

@dataclass
class DailyIntake:
    owner_id: int
    calories: float
    fat_g: float
    sugar_g: float
    protein_g: float

    def to_dict(self):
        return asdict(self)