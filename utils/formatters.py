def format_kcal(value: float) -> str:
    return f"{int(round(value)):,} ккал".replace(",", "\u00a0")


def format_grams(value: float) -> str:
    return f"{value:.1f} г"
