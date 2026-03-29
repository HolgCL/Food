import plotly.graph_objects as go
import streamlit as st

from calculators.kbju import (
    MIN_SAFE_CALORIES,
    bmi_category,
    calculate_bmi,
    calculate_bmr,
    calculate_daily_deficit,
    calculate_macros,
    calculate_target_calories,
    calculate_tdee,
    ideal_weight_range,
    steps_to_activity_multiplier,
    weight_projection,
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
    pcts = [k / target_cal * 100 if target_cal else 0 for k in kcals]
    hover_texts = [
        f"<b>{lb}</b><br>{g:.1f} г<br>{k:.0f} ккал<br>{p:.1f}% от суточной нормы"
        for lb, g, k, p in zip(labels, grams, kcals, pcts)
    ]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=kcals,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#1e1e1e", width=2)),
        textinfo="label+percent",
        textfont=dict(size=13),
        text=hover_texts,
        hovertemplate="%{text}<extra></extra>",
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


def _weight_chart(weight: float, deficit_per_day: float, period_days: int, height_cm: float) -> go.Figure:
    points = weight_projection(weight, deficit_per_day, period_days)
    weeks  = [p[0] for p in points]
    weights = [p[1] for p in points]
    ideal_min, ideal_max = ideal_weight_range(height_cm)

    y_min = min(min(weights) * 0.98, ideal_min * 0.98)
    y_max = max(max(weights) * 1.01, ideal_max * 1.01)

    fig = go.Figure()

    # Ideal weight band
    fig.add_hrect(
        y0=ideal_min, y1=ideal_max,
        fillcolor="#1a3a1a", opacity=0.5, line_width=0,
        annotation_text=f"Идеальный вес ({ideal_min}–{ideal_max} кг)",
        annotation_position="top right",
        annotation_font=dict(color="#58C4A0", size=11),
    )

    hover = [f"<b>Неделя {w:.0f}</b><br>Вес: {wt:.1f} кг" for w, wt in zip(weeks, weights)]

    fig.add_trace(go.Scatter(
        x=weeks, y=weights,
        mode="lines+markers",
        line=dict(color="#4C9BE8", width=3),
        marker=dict(size=6, color="#4C9BE8"),
        hovertext=hover,
        hovertemplate="%{hovertext}<extra></extra>",
        name="Вес",
    ))

    fig.add_annotation(x=0, y=weights[0],
                       text=f"  {weights[0]} кг",
                       showarrow=False, font=dict(size=12, color="white"), xanchor="left")
    fig.add_annotation(x=weeks[-1], y=weights[-1],
                       text=f"  {weights[-1]} кг",
                       showarrow=False, font=dict(size=12, color="#4C9BE8"), xanchor="left")

    fig.update_layout(
        xaxis_title="Недели",
        yaxis_title="Вес (кг)",
        yaxis=dict(range=[y_min, y_max], gridcolor="#333"),
        xaxis=dict(gridcolor="#333"),
        height=280,
        margin=dict(t=20, b=30, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=False,
        hoverlabel=dict(bgcolor="#2b2b2b", font_color="white", font_size=13, bordercolor="#555"),
    )
    return fig


def _export_text(data: dict) -> str:
    lines = [
        "РАСЧЁТ КБЖУ",
        "=" * 32,
        f"Пол: {'Мужской' if data['gender'] == 'male' else 'Женский'}",
        f"Возраст: {data['age']} лет",
        f"Вес: {data['weight']} кг  |  Рост: {data['height']} см",
        f"Шаги в день: {data['steps']}",
        f"Цель: -{data['target_loss']} кг за {data['period_days']} дней",
        "",
        "РЕЗУЛЬТАТ:",
        f"Калории:   {int(data['target_cal'])} ккал/день",
        f"Белки:     {data['macros']['protein']} г",
        f"Жиры:      {data['macros']['fat']} г",
        f"Углеводы:  {data['macros']['carbs']} г",
        "",
        f"BMR:     {int(data['bmr'])} ккал",
        f"TDEE:    {int(data['tdee'])} ккал",
        f"Дефицит: {int(data['daily_deficit'])} ккал/день",
        f"ИМТ:     {data['bmi']:.1f} ({data['bmi_label']})",
        f"Идеальный вес: {data['ideal_min']}–{data['ideal_max']} кг",
    ]
    return "\n".join(lines)


def render_calculator_tab() -> None:
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] { font-size: 1.2rem; }
        </style>
    """, unsafe_allow_html=True)
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
            min_value=0, max_value=20_000, value=7_500, step=500,
            format="%d шагов",
        )

        st.subheader("Цель")
        target_loss = st.number_input(
            "Хочу похудеть на (кг)", min_value=0.1, max_value=100.0, value=5.0, step=0.5
        )
        period_unit = st.radio("Период", ["Недели", "Дни"], horizontal=True)
        period_val = st.number_input("Количество", min_value=1, max_value=365, value=8)

    period_days = period_val * 7 if period_unit == "Недели" else period_val

    bmr          = calculate_bmr(weight, height, age, gender)
    multiplier   = steps_to_activity_multiplier(steps)
    tdee         = calculate_tdee(bmr, multiplier)
    daily_deficit = calculate_daily_deficit(target_loss, period_days)
    target_cal   = calculate_target_calories(tdee, daily_deficit)
    macros       = calculate_macros(target_cal, weight)
    bmi          = calculate_bmi(weight, height)
    bmi_label, bmi_color = bmi_category(bmi)
    ideal_min, ideal_max = ideal_weight_range(height)

    # Save goals to session state for diary tab
    st.session_state.kbju_goals = {
        "calories": target_cal,
        "protein":  macros["protein"],
        "fat":      macros["fat"],
        "carbs":    macros["carbs"],
    }

    with col_results:
        st.subheader("Результат")

        if daily_deficit > tdee * 0.5:
            st.warning(
                f"Цель слишком агрессивная: дефицит **{format_kcal(daily_deficit)}** в день "
                f"превышает половину TDEE. Увеличьте период или уменьшите целевой вес."
            )
        floored = (tdee - daily_deficit) < MIN_SAFE_CALORIES and target_loss > 0
        if floored:
            st.warning(
                f"Калорийность ниже минимума — зафиксировано на **{MIN_SAFE_CALORIES} ккал**."
            )

        # КБЖУ metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Калории", format_kcal(target_cal))
        m2.metric("Белки", format_grams(macros["protein"]))
        m3.metric("Жиры", format_grams(macros["fat"]))
        m4.metric("Углеводы", format_grams(macros["carbs"]))

        # BMI row
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("ИМТ", f"{bmi:.1f}")
        b2.metric("Категория", bmi_label)
        b3.metric("Идеальный вес", f"{ideal_min}–{ideal_max} кг")
        diff = round(weight - ideal_max, 1)
        b4.metric("До нормы", f"{diff:+.1f} кг" if diff != 0 else "В норме")

        st.divider()

        activity_label = _ACTIVITY_LABELS.get(multiplier, "")
        st.info(
            f"**BMR:** {format_kcal(bmr)}  \n"
            f"**TDEE:** {format_kcal(tdee)} — {activity_label}  \n"
            f"**Дефицит:** {format_kcal(daily_deficit)}/день  \n"
            f"**Период:** {period_days} дней"
        )

        c1, c2 = st.columns([3, 2])
        with c1:
            st.caption("Распределение калорий по макронутриентам")
            st.plotly_chart(_donut_chart(macros, target_cal), use_container_width=True)
        with c2:
            st.plotly_chart(_energy_gauge(target_cal, tdee), use_container_width=True)

    # Weight projection chart (full width)
    st.divider()
    st.subheader("Прогноз веса")
    st.plotly_chart(_weight_chart(weight, daily_deficit, period_days, height), use_container_width=True)

    # Export + History row
    col_export, col_hist_btn, _ = st.columns([1, 1, 2])

    export_data = {
        "gender": gender, "age": age, "weight": weight, "height": height,
        "steps": steps, "target_loss": target_loss, "period_days": period_days,
        "bmr": bmr, "tdee": tdee, "daily_deficit": daily_deficit,
        "target_cal": target_cal, "macros": macros,
        "bmi": bmi, "bmi_label": bmi_label,
        "ideal_min": ideal_min, "ideal_max": ideal_max,
    }

    with col_export:
        st.download_button(
            label="Скачать расчёт",
            data=_export_text(export_data),
            file_name="kbju_расчёт.txt",
            mime="text/plain",
        )

    with col_hist_btn:
        if st.button("Сохранить в историю"):
            if "calc_history" not in st.session_state:
                st.session_state.calc_history = []
            st.session_state.calc_history.insert(0, export_data.copy())
            st.session_state.calc_history = st.session_state.calc_history[:5]
            st.toast("Расчёт сохранён в историю")

    # History
    history = st.session_state.get("calc_history", [])
    if history:
        with st.expander(f"История расчётов ({len(history)})"):
            for i, h in enumerate(history):
                gender_str = "М" if h["gender"] == "male" else "Ж"
                st.markdown(
                    f"**{i+1}.** {gender_str}, {h['age']}л, {h['weight']}кг, {h['height']}см — "
                    f"цель: −{h['target_loss']}кг за {h['period_days']}дней → "
                    f"**{int(h['target_cal'])} ккал** "
                    f"(Б:{h['macros']['protein']}г Ж:{h['macros']['fat']}г У:{h['macros']['carbs']}г)"
                )
