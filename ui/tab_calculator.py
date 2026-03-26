import streamlit as st

from calculators.kbju import (
    MIN_SAFE_CALORIES,
    calculate_bmr,
    calculate_daily_deficit,
    calculate_macros,
    calculate_target_calories,
    calculate_tdee,
    steps_to_activity_multiplier,
)
from utils.formatters import format_grams, format_kcal

_ACTIVITY_LABELS = {
    1.200: "Сидячий образ жизни",
    1.375: "Слабоактивный",
    1.550: "Умеренно активный",
    1.725: "Высокоактивный",
    1.900: "Очень высокоактивный",
}


def render_calculator_tab() -> None:
    st.header("Расчёт КБЖУ для похудения")

    col_inputs, col_results = st.columns([1, 1], gap="large")

    with col_inputs:
        st.subheader("Параметры тела")
        gender_label = st.radio("Пол", ["Мужской", "Женский"], horizontal=True)
        gender = "male" if gender_label == "Мужской" else "female"

        age = st.number_input("Возраст (лет)", min_value=14, max_value=100, value=30)
        weight = st.number_input(
            "Текущий вес (кг)", min_value=30.0, max_value=250.0, value=75.0, step=0.5
        )
        height = st.number_input(
            "Рост (см)", min_value=140, max_value=220, value=175
        )

        steps = st.slider(
            "Среднее кол-во шагов в день",
            min_value=0,
            max_value=20_000,
            value=7_500,
            step=500,
            format="%d шагов",
        )

        st.subheader("Цель")
        target_loss = st.number_input(
            "Хочу похудеть на (кг)",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.5,
        )
        period_unit = st.radio("Период", ["Недели", "Дни"], horizontal=True)
        period_val = st.number_input(
            "Количество",
            min_value=1,
            max_value=365,
            value=8,
        )

    period_days = period_val * 7 if period_unit == "Недели" else period_val

    bmr = calculate_bmr(weight, height, age, gender)
    multiplier = steps_to_activity_multiplier(steps)
    tdee = calculate_tdee(bmr, multiplier)
    daily_deficit = calculate_daily_deficit(target_loss, period_days)
    target_cal = calculate_target_calories(tdee, daily_deficit)
    macros = calculate_macros(target_cal, weight)

    with col_results:
        st.subheader("Результат")

        # Warnings
        if daily_deficit > tdee * 0.5:
            st.warning(
                f"Цель слишком агрессивная: требуемый дефицит "
                f"**{format_kcal(daily_deficit)}** в день превышает половину вашего TDEE. "
                f"Рекомендуем увеличить период или уменьшить целевой вес."
            )

        floored = (tdee - daily_deficit) < MIN_SAFE_CALORIES and target_loss > 0
        if floored:
            st.warning(
                f"Расчётная калорийность опускается ниже безопасного минимума — "
                f"зафиксировано на **{MIN_SAFE_CALORIES} ккал**."
            )

        # Key metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Калории", format_kcal(target_cal))
        m2.metric("Белки", format_grams(macros["protein"]))
        m3.metric("Жиры", format_grams(macros["fat"]))
        m4.metric("Углеводы", format_grams(macros["carbs"]))

        st.divider()

        # Intermediate values
        activity_label = _ACTIVITY_LABELS.get(multiplier, "")
        st.info(
            f"**Базовый обмен (BMR):** {format_kcal(bmr)}  \n"
            f"**Суточный расход (TDEE):** {format_kcal(tdee)} — {activity_label}  \n"
            f"**Дефицит в день:** {format_kcal(daily_deficit)}  \n"
            f"**Период:** {period_days} дней"
        )

        # Macro calorie breakdown bar chart
        st.caption("Распределение калорий по макронутриентам")
        macro_cal = {
            "Белки": macros["protein"] * 4,
            "Жиры": macros["fat"] * 9,
            "Углеводы": macros["carbs"] * 4,
        }
        st.bar_chart(macro_cal, use_container_width=True, height=200)
