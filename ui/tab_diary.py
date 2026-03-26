import streamlit as st

from data.foods import FOODS

_FOODS_MAP = {f["name"]: f for f in FOODS}
_FOOD_NAMES = sorted(f["name"] for f in FOODS)


def _init() -> None:
    if "diary" not in st.session_state:
        st.session_state.diary = []


def _add_entry(name: str, grams: float) -> None:
    food = _FOODS_MAP[name]
    ratio = grams / 100
    st.session_state.diary.append({
        "name":     name,
        "grams":    grams,
        "calories": round(food["calories"] * ratio, 1),
        "protein":  round(food["protein"] * ratio, 1),
        "fat":      round(food["fat"] * ratio, 1),
        "carbs":    round(food["carbs"] * ratio, 1),
        "fiber":    round(food["fiber"] * ratio, 1),
    })


def _progress(label: str, current: float, goal: float, unit: str) -> None:
    pct = min(current / goal, 1.0) if goal > 0 else 0
    over = current > goal
    st.write(
        f"**{label}:** {current:.0f} / {goal:.0f} {unit} "
        f"({'⚠️ превышено' if over else f'{pct*100:.0f}%'})"
    )
    st.progress(pct)


def render_diary_tab() -> None:
    st.header("Дневник питания")
    _init()

    # Add food form
    col_food, col_g, col_btn = st.columns([3, 1, 1])
    with col_food:
        food_name = st.selectbox("Продукт", _FOOD_NAMES, label_visibility="collapsed", key="diary_food")
    with col_g:
        grams = st.number_input("г", min_value=1, max_value=3000, value=100,
                                label_visibility="collapsed", key="diary_grams")
    with col_btn:
        if st.button("+ Добавить", use_container_width=True):
            _add_entry(food_name, grams)
            st.rerun()

    if not st.session_state.diary:
        st.info("Дневник пуст — добавьте первый продукт выше")
        return

    st.divider()
    st.subheader("Съедено сегодня")

    for i, entry in enumerate(st.session_state.diary):
        c1, c2, c3, c4, c5, c6 = st.columns([3, 1, 1, 1, 1, 0.5])
        c1.write(f"**{entry['name']}** ({entry['grams']} г)")
        c2.write(f"{entry['calories']:.0f} ккал")
        c3.write(f"Б {entry['protein']:.1f} г")
        c4.write(f"Ж {entry['fat']:.1f} г")
        c5.write(f"У {entry['carbs']:.1f} г")
        if c6.button("✕", key=f"del_{i}"):
            st.session_state.diary.pop(i)
            st.rerun()

    st.divider()

    total_cal     = sum(e["calories"] for e in st.session_state.diary)
    total_protein = sum(e["protein"]  for e in st.session_state.diary)
    total_fat     = sum(e["fat"]      for e in st.session_state.diary)
    total_carbs   = sum(e["carbs"]    for e in st.session_state.diary)
    total_fiber   = sum(e["fiber"]    for e in st.session_state.diary)

    st.subheader("Итого за день")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Калории",   f"{int(total_cal)} ккал")
    m2.metric("Белки",     f"{total_protein:.1f} г")
    m3.metric("Жиры",      f"{total_fat:.1f} г")
    m4.metric("Углеводы",  f"{total_carbs:.1f} г")
    m5.metric("Клетчатка", f"{total_fiber:.1f} г")

    goals = st.session_state.get("kbju_goals", {})
    if goals:
        st.subheader("Прогресс по цели")
        _progress("Калории",  total_cal,     goals.get("calories", 0), "ккал")
        _progress("Белки",    total_protein, goals.get("protein", 0),  "г")
        _progress("Жиры",     total_fat,     goals.get("fat", 0),      "г")
        _progress("Углеводы", total_carbs,   goals.get("carbs", 0),    "г")
    else:
        st.info("Рассчитайте КБЖУ на первом табе, чтобы видеть прогресс по цели")

    st.divider()
    if st.button("Очистить дневник", type="secondary"):
        st.session_state.diary = []
        st.rerun()
