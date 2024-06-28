from passlib import hash
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    calories = relationship("UserCalories", back_populates="owner")
    food_info = relationship("FoodInfoDB", back_populates="owner")
    user_metrics = relationship("UserMetricsDB", back_populates="owner")  # Změněno z UserMetrics na UserMetricsDB

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password.encode('utf-8'), self.hashed_password)


class UserMetricsDB(Base):
    __tablename__ = "user_metrics"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    age = Column(Float, nullable=False)
    gender = Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now(timezone.utc))
    date_last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="user_metrics")


class UserCalories(Base):
    __tablename__ = "user_calories"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    calories = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    sugar_g = Column(Float, nullable=False)
    protein_g = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime.now(timezone.utc))
    date_last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="calories")


class FoodInfoDB(Base):
    __tablename__ = "food_info"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    certainty = Column(Float, nullable=False)
    food_name = Column(String, nullable=False)
    calories_Kcal = Column(Float, nullable=False)
    fat_in_g = Column(Float, nullable=False)
    sugar_in_g = Column(Float, nullable=False)
    protein_in_g = Column(Float, nullable=False)
    date_created = Column(DateTime, default=datetime.now(timezone.utc))
    date_last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="food_info")
