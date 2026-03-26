FOODS: list[dict] = [
    # Мясо
    {"name": "Куриная грудка",       "calories": 165, "protein": 31.0, "fat":  3.6, "carbs":  0.0, "fiber": 0.0, "category": "Мясо"},
    {"name": "Куриное бедро",        "calories": 215, "protein": 26.0, "fat": 12.0, "carbs":  0.0, "fiber": 0.0, "category": "Мясо"},
    {"name": "Говядина постная",     "calories": 218, "protein": 26.1, "fat": 12.7, "carbs":  0.0, "fiber": 0.0, "category": "Мясо"},
    {"name": "Свинина постная",      "calories": 242, "protein": 27.0, "fat": 14.0, "carbs":  0.0, "fiber": 0.0, "category": "Мясо"},
    {"name": "Индейка",              "calories": 189, "protein": 28.6, "fat":  7.4, "carbs":  0.0, "fiber": 0.0, "category": "Мясо"},

    # Рыба и морепродукты
    {"name": "Лосось",               "calories": 208, "protein": 20.1, "fat": 13.4, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},
    {"name": "Тунец в воде",         "calories": 116, "protein": 25.5, "fat":  1.0, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},
    {"name": "Треска",               "calories":  82, "protein": 17.8, "fat":  0.7, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},
    {"name": "Минтай",               "calories":  72, "protein": 15.9, "fat":  0.9, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},
    {"name": "Скумбрия",             "calories": 205, "protein": 18.0, "fat": 13.2, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},
    {"name": "Креветки варёные",     "calories":  99, "protein": 20.9, "fat":  1.1, "carbs":  0.0, "fiber": 0.0, "category": "Рыба"},

    # Молочное и яйца
    {"name": "Яйцо куриное",         "calories": 155, "protein": 12.6, "fat": 10.6, "carbs":  1.1, "fiber": 0.0, "category": "Молочное"},
    {"name": "Творог 0%",            "calories":  71, "protein": 16.5, "fat":  0.1, "carbs":  1.3, "fiber": 0.0, "category": "Молочное"},
    {"name": "Творог 5%",            "calories": 121, "protein": 17.0, "fat":  5.0, "carbs":  1.8, "fiber": 0.0, "category": "Молочное"},
    {"name": "Молоко 2.5%",          "calories":  52, "protein":  2.9, "fat":  2.5, "carbs":  4.8, "fiber": 0.0, "category": "Молочное"},
    {"name": "Кефир 1%",             "calories":  40, "protein":  3.2, "fat":  1.0, "carbs":  4.1, "fiber": 0.0, "category": "Молочное"},
    {"name": "Греческий йогурт 0%",  "calories":  59, "protein": 10.0, "fat":  0.4, "carbs":  3.6, "fiber": 0.0, "category": "Молочное"},
    {"name": "Сыр твёрдый",          "calories": 364, "protein": 25.0, "fat": 28.0, "carbs":  2.0, "fiber": 0.0, "category": "Молочное"},

    # Крупы и злаки
    {"name": "Гречка варёная",       "calories": 110, "protein":  4.2, "fat":  1.1, "carbs": 21.3, "fiber": 2.7, "category": "Крупы"},
    {"name": "Рис белый варёный",    "calories": 130, "protein":  2.7, "fat":  0.3, "carbs": 28.2, "fiber": 0.4, "category": "Крупы"},
    {"name": "Рис бурый варёный",    "calories": 112, "protein":  2.6, "fat":  0.9, "carbs": 23.0, "fiber": 1.8, "category": "Крупы"},
    {"name": "Овсянка варёная",      "calories":  71, "protein":  2.5, "fat":  1.5, "carbs": 12.0, "fiber": 1.7, "category": "Крупы"},
    {"name": "Макароны варёные",     "calories": 158, "protein":  5.8, "fat":  0.9, "carbs": 30.9, "fiber": 1.8, "category": "Крупы"},
    {"name": "Перловка варёная",     "calories": 123, "protein":  2.3, "fat":  0.4, "carbs": 28.2, "fiber": 3.8, "category": "Крупы"},

    # Овощи
    {"name": "Брокколи",             "calories":  34, "protein":  2.8, "fat":  0.4, "carbs":  6.6, "fiber": 2.6, "category": "Овощи"},
    {"name": "Огурец",               "calories":  15, "protein":  0.7, "fat":  0.1, "carbs":  3.6, "fiber": 0.5, "category": "Овощи"},
    {"name": "Помидор",              "calories":  18, "protein":  0.9, "fat":  0.2, "carbs":  3.9, "fiber": 1.2, "category": "Овощи"},
    {"name": "Капуста белокочанная", "calories":  25, "protein":  1.3, "fat":  0.1, "carbs":  5.8, "fiber": 2.0, "category": "Овощи"},
    {"name": "Морковь",              "calories":  41, "protein":  0.9, "fat":  0.2, "carbs":  9.6, "fiber": 2.8, "category": "Овощи"},
    {"name": "Болгарский перец",     "calories":  31, "protein":  1.0, "fat":  0.3, "carbs":  6.0, "fiber": 2.1, "category": "Овощи"},
    {"name": "Шпинат",               "calories":  23, "protein":  2.9, "fat":  0.4, "carbs":  3.6, "fiber": 2.2, "category": "Овощи"},

    # Фрукты
    {"name": "Яблоко",               "calories":  52, "protein":  0.3, "fat":  0.2, "carbs": 13.8, "fiber": 2.4, "category": "Фрукты"},
    {"name": "Банан",                "calories":  89, "protein":  1.1, "fat":  0.3, "carbs": 22.8, "fiber": 2.6, "category": "Фрукты"},
    {"name": "Апельсин",             "calories":  47, "protein":  0.9, "fat":  0.1, "carbs": 11.8, "fiber": 2.4, "category": "Фрукты"},
    {"name": "Клубника",             "calories":  32, "protein":  0.7, "fat":  0.3, "carbs":  7.7, "fiber": 2.0, "category": "Фрукты"},
    {"name": "Черника",              "calories":  57, "protein":  0.7, "fat":  0.3, "carbs": 14.5, "fiber": 2.4, "category": "Фрукты"},

    # Бобовые
    {"name": "Чечевица варёная",     "calories": 116, "protein":  9.0, "fat":  0.4, "carbs": 20.1, "fiber": 7.9, "category": "Бобовые"},
    {"name": "Нут варёный",          "calories": 164, "protein":  8.9, "fat":  2.6, "carbs": 27.4, "fiber": 7.6, "category": "Бобовые"},
    {"name": "Фасоль варёная",       "calories": 127, "protein":  8.7, "fat":  0.5, "carbs": 22.8, "fiber": 6.4, "category": "Бобовые"},
]
