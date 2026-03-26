import pandas as pd
import streamlit as st

from data.foods import FOODS

_COLUMN_MAP = {
    "name":     "Продукт",
    "calories": "Калории",
    "protein":  "Белки (г)",
    "fat":      "Жиры (г)",
    "carbs":    "Углеводы (г)",
    "fiber":    "Клетчатка (г)",
    "category": "Категория",
}


def render_food_db_tab() -> None:
    st.header("База продуктов")
    st.caption("Все значения указаны на 100 г продукта")

    df = pd.DataFrame(FOODS).rename(columns=_COLUMN_MAP)

    col_search, col_cat = st.columns([2, 1])
    with col_search:
        search = st.text_input("Поиск", placeholder="Например: куриная, рис...")
    with col_cat:
        categories = ["Все"] + sorted(df["Категория"].unique().tolist())
        selected_cat = st.selectbox("Категория", categories)

    mask = pd.Series([True] * len(df), index=df.index)
    if search:
        mask &= df["Продукт"].str.contains(search, case=False, na=False)
    if selected_cat != "Все":
        mask &= df["Категория"] == selected_cat

    filtered = df[mask]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Калории":      st.column_config.NumberColumn(format="%d ккал"),
            "Белки (г)":    st.column_config.NumberColumn(format="%.1f г"),
            "Жиры (г)":     st.column_config.NumberColumn(format="%.1f г"),
            "Углеводы (г)": st.column_config.NumberColumn(format="%.1f г"),
            "Клетчатка (г)":st.column_config.NumberColumn(format="%.1f г"),
        },
    )
    st.caption(f"Показано {len(filtered)} из {len(df)} продуктов")
