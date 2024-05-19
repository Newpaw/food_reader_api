from .models import UserInfo, DailyIntake

# Define the IntakeCalculator class

class IntakeCalculator:
    @staticmethod
    def calculate_daily_intake(user_info: UserInfo) -> DailyIntake:
        if user_info.gender == "male":
            bmr = 88.362 + (13.397 * user_info.weight_kg) + (4.799 * user_info.height_cm) - (5.677 * user_info.age)
        else:
            bmr = 447.593 + (9.247 * user_info.weight_kg) + (3.098 * user_info.height_cm) - (4.330 * user_info.age)

        activity_factors = {
            "low": 1.2,
            "medium": 1.55,
            "high": 1.725
        }

        daily_calories = bmr * activity_factors[user_info.activity_level]
        
        protein_g = user_info.weight_kg * 1.2
        fat_g = daily_calories * 0.25 / 9
        sugar_g = daily_calories * 0.1 / 4

        return DailyIntake(
            user_id=user_info.user_id,
            calories=daily_calories,
            fat_g=fat_g,
            sugar_g=sugar_g,
            protein_g=protein_g
        )
