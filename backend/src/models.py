from dataclasses import dataclass, asdict
from sqlalchemy import Column, Integer, Float, String

from .database import Base


@dataclass
class FoodInfo:
    certainty: float | int
    food_name: str
    calories_Kcal: float | int
    fat_in_g: float | int
    protein_in_g: float | int
    sugar_in_g: float | int

    def to_dict(self):
        return asdict(self)


class ColoriesToDB(Base):
    __tablename__ = "user_calories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    calories = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    sugar_g = Column(Float, nullable=False)
    protein_g = Column(Float, nullable=False)


class FoodInfoToDB(Base):
    __tablename__ = "food_info"
    id = Column(Integer, primary_key=True, index=True)
    certainty = Column(Float, nullable=False)
    food_name = Column(String, nullable=False)
    calories_Kcal = Column(Float, nullable=False)
    fat_in_g = Column(Float, nullable=False)
    sugar_in_g = Column(Float, nullable=False)
    protein_in_g = Column(Float, nullable=False)