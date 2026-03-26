import plotly.graph_objects as go
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

_MACRO_COLORS = {
    "Белки":    "#4C9BE8",
    "Жиры":     "#F4845F",
    "Углеводы": "#58C4A0",
}


def _donut_chart(macros: dict, target_cal: float) -> go.Figure:
    labels = ["Белки", "Жиры", "Углеводы"]
    grams  = [macros["protein"], macros["fat"], macros["carbs"]]
    kcals  = [macros["protein"] * 4, macros["fat"] * 9, macros["carbs"] * 4]
    colors = [_MACRO_COLORS[l] for l in labels]
    pcts   = [k / target_cal * 100 if target_cal else 0 for k in kcals]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=kcals,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#1e1e1e", width=2)),
        textinfo="label+percent",
        textfont=dict(size=13),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{customdata[0]:.1f} г<br>"
            "%{value:.0f} ккал<br>"
            "%{customdata[1]:.1f}% от суточной нормы"
            "<extra></extra>"
        ),
        customdata=list(zip(grams, pcts)),
    ))

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{int(round(target_cal))}</b><br>ккал",
            x=0.5, y=0.5,
            font=dict(size=18),
            showarrow=False,
        )],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(t=10, b=10, l=10, r=10),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
    )
    return fig


def _energy_gauge(target_cal: float, tdee: float) -> go.Figure:
    pct = min(target_cal / tdee * 100, 100) if tdee else 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=target_cal,
        delta=dict(
            reference=tdee,
            valueformat=".0f",
            suffix=" ккал",
            increasing=dict(color="#F4845F"),
            decreasing=dict(color="#58C4A0"),
        ),
        number=dict(suffix=" ккал", font=dict(size=22)),
        gauge=dict(
            axis=dict(range=[0, tdee * 1.1], ticksuffix=" ккал", tickfont=dict(size=10)),
            bar=dict(color="#4C9BE8", thickness=0.25),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0, MIN_SAFE_CALORIES], color="#3a1a1a"),
                dict(range=[MIN_SAFE_CALORIES, tdee * 0.7], color="#2a3a2a"),
                dict(range=[tdee * 0.7, tdee], color="#1e2e1e"),
            ],
            threshold=dict(
                line=dict(color="#F4845F", width=3),
                thickness=0.8,
                value=tdee,
            ),
        ),
        title=dict(text="Цель vs TDEE", font=dict(size=14)),
    ))

    fig.update_layout(
        height=220,
        margin=dict(t=40, b=10, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white"),
    )
    return fig


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
        height = st.number_input("Рост (см)", min_value=140, max_value=220, value=175)

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
            "Хочу похудеть на (кг)", min_value=0.1, max_value=100.0, value=5.0, step=0.5
        )
        period_unit = st.radio("Период", ["Недели", "Дни"], horizontal=True)
        period_val = st.number_input("Количество", min_value=1, max_value=365, value=8)

    period_days = period_val * 7 if period_unit == "Недели" else period_val

    bmr = calculate_bmr(weight, height, age, gender)
    multiplier = steps_to_activity_multiplier(steps)
    tdee = calculate_tdee(bmr, multiplier)
    daily_deficit = calculate_daily_deficit(target_loss, period_days)
    target_cal = calculate_target_calories(tdee, daily_deficit)
    macros = calculate_macros(target_cal, weight)

    with col_results:
        st.subheader("Результат")

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

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Калории", format_kcal(target_cal))
        m2.metric("Белки", format_grams(macros["protein"]))
        m3.metric("Жиры", format_grams(macros["fat"]))
        m4.metric("Углеводы", format_grams(macros["carbs"]))

        st.divider()

        activity_label = _ACTIVITY_LABELS.get(multiplier, "")
        st.info(
            f"**Базовый обмен (BMR):** {format_kcal(bmr)}  \n"
            f"**Суточный расход (TDEE):** {format_kcal(tdee)} — {activity_label}  \n"
            f"**Дефицит в день:** {format_kcal(daily_deficit)}  \n"
            f"**Период:** {period_days} дней"
        )

        c1, c2 = st.columns([3, 2])
        with c1:
            st.caption("Распределение калорий по макронутриентам")
            st.plotly_chart(_donut_chart(macros, target_cal), use_container_width=True)
        with c2:
            st.plotly_chart(_energy_gauge(target_cal, tdee), use_container_width=True)
