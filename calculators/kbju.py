_STEPS_MULTIPLIERS = [
    (3_500,       1.200),
    (7_500,       1.375),
    (10_000,      1.550),
    (12_500,      1.725),
    (float("inf"), 1.900),
]

KCAL_PER_KG_FAT = 7700
MIN_SAFE_CALORIES = 1200


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if gender == "male" else base - 161


def steps_to_activity_multiplier(steps: int) -> float:
    for threshold, multiplier in _STEPS_MULTIPLIERS:
        if steps < threshold:
            return multiplier
    return 1.900


def calculate_tdee(bmr: float, activity_multiplier: float) -> float:
    return bmr * activity_multiplier


def calculate_daily_deficit(target_loss_kg: float, period_days: int) -> float:
    if period_days <= 0:
        return 0.0
    return (target_loss_kg * KCAL_PER_KG_FAT) / period_days


def calculate_target_calories(tdee: float, daily_deficit: float) -> float:
    return max(tdee - daily_deficit, MIN_SAFE_CALORIES)


def calculate_macros(target_calories: float, weight_kg: float) -> dict:
    protein_g = weight_kg * 2
    fat_g = (target_calories * 0.25) / 9
    carbs_g = max((target_calories - protein_g * 4 - fat_g * 9) / 4, 0)
    return {
        "protein": round(protein_g, 1),
        "fat": round(fat_g, 1),
        "carbs": round(carbs_g, 1),
    }


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    return weight_kg / (height_cm / 100) ** 2


def bmi_category(bmi: float) -> tuple[str, str]:
    """Returns (label, color)."""
    if bmi < 18.5:
        return "Дефицит веса", "#5A9BE0"
    elif bmi < 25.0:
        return "Норма", "#58C4A0"
    elif bmi < 30.0:
        return "Избыточный вес", "#E0C95A"
    return "Ожирение", "#E07B5A"


def ideal_weight_range(height_cm: float) -> tuple[float, float]:
    h = height_cm / 100
    return round(18.5 * h ** 2, 1), round(24.9 * h ** 2, 1)


def weight_projection(weight: float, deficit_per_day: float, period_days: int) -> list[tuple[float, float]]:
    """Returns list of (week, weight_kg) tuples."""
    loss_per_day = deficit_per_day / KCAL_PER_KG_FAT
    step = max(1, period_days // 20)
    days = list(range(0, period_days + 1, step))
    if days[-1] != period_days:
        days.append(period_days)
    return [(d / 7, round(weight - loss_per_day * d, 2)) for d in days]
